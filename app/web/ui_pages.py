"""NiceGUI pages for the editor web app (docs/01_technical.md §2.3, §2.6; build plan Phase 3/4).

This module owns the UI LAYER. The owner picked NiceGUI as the ready SDK so we don't hand-roll
templates; importing this module registers the two `@ui.page(...)` functions on the global
NiceGUI app, which `app/web/routes.py` then mounts onto the existing FastAPI instance via
`ui.run_with(...)`. The backend is unchanged and reused: this file only READS the DB (clusters +
articles via app.web.queries) and CALLS shared components (app.editor for create+draft+approve,
the app.web.chat seam for iterate) — it never calls the poller/bot/researcher.

Two pages:
  - `@ui.page('/')` — admin / dashboard: pipeline counts, the "ready to draft" list (with the
    Draft action that runs the writer-agent), and a minimal read-only browse of recent rows.
  - `@ui.page('/editor/{article_id}')` — the chat-drafting surface: a two-pane split of a chat
    (left) and a live markdown preview + raw hand-edit textarea (right), plus the Phase-4
    controls — the piece-type switcher (mid-stream reformat) and the Gate-2 Approve control.

Phase 4 lit up the BRAIN side of the editor:
  - Chat iterate is wired to the writer-agent ITERATE seam (`chat_seam.handle_editor_message`).
    The owner's UNSAVED textarea value is passed as `base_draft` so manual hand-edits are the
    base the agent edits in place (respect manual edits — hard rule). On return the live preview
    AND the raw textarea refresh from the FULL revised draft (edit-in-place, never regeneration).
  - A piece-type switcher (`ui.select` of PIECE_TYPES) routes a mid-stream reformat through the
    same seam with `new_piece_type=…` (a structural reformat, not a point edit).
  - A Gate-2 "Approve (pre-publish)" control calls `approve_article` (drafting → pre_publish).
    This is owner approval of the canonical — NOT publishing; nothing is ever posted.

Phase 5 (this slice) closes the lifecycle — still WITHOUT ever posting:
  - A "Mark as published" header control (next to Approve) calls `app.editor.publish_article`
    (pre_publish → published + builds the KB embedding). It is BOOKKEEPING of an external,
    MANUAL publish the owner already did elsewhere — it flips a DB status and populates the
    knowledge base; it does NOT post anywhere. It is meaningful only after Gate 2: enabled at
    `pre_publish`, disabled while `drafting`/`approved` (approve first) and once `published`.
  - A Variants section in the preview pane: per platform (Medium / Reddit / LinkedIn) a
    "Generate" button that calls `app.variants.generate_variant` (ONE model call), an EDITABLE
    output area the owner SELECTS + COPIES to post MANUALLY (and can hand-tune inline), and a
    "Save" button that persists that hand-tuned text back via `app.variants.save_variant_edit`
    (a plain DB write — NO model call, never posts). Variants are derived AFTER Gate 2, so the
    Generate + Save buttons are enabled only at `pre_publish`/`published`. They are displayed for
    copy-out only — no posting buttons, no share integrations, ever.
  Cross-control wiring: a successful Gate-2 Approve flips this page from `drafting` to
  `pre_publish`, so it ENABLES the mark-published button and the variant generate buttons in
  place; a successful Mark-as-published disables the mark-published button (already published).

House rules honoured here:
  - NEVER publishes — this is a preview/editing/admin surface; no posting path exists. "Mark as
    published" only records that the owner published manually (status bookkeeping + KB embedding);
    the variants are copy-out text only. The system never posts.
  - NO auth in the app — Caddy fronts `web` with HTTP basic auth (docs/02_infra.md §5). The
    NiceGUI `storage_secret` is only cookie-signing, not authentication.
  - Grounding stays in the editor backend — we CALL `draft_article` / `handle_editor_message` /
    `generate_variant` / `publish_article`; we do not weaken its provenance/flag-unverified/
    propose-not-assert enforcement, and we surface its refusals (e.g. grounding ValueError, a
    non-pre_publish publish, an empty-draft variant) as a clear notify.
  - Postgres-only coordination — every read/write goes through a short-lived DB session.

Heavy/optional imports (app.editor → the LLM/agent stack) are LAZY inside the click handlers so
importing this module (uvicorn boot, test collection) stays cheap and side-effect-free apart
from registering the pages. Blocking work (the writer-agent draft/iterate, Gate-2 approve) is
pushed off the event loop with `run.io_bound(...)` so it never freezes the UI for the single owner.
"""
from __future__ import annotations

import difflib
import html as _html
import logging
import re
from collections.abc import Callable, Iterator
from contextlib import contextmanager

from nicegui import run, ui

from app.web import chat as chat_seam
from app.web import queries

log = logging.getLogger("web.ui")

# Empty-draft placeholder shown in the preview pane before the writer-agent has drafted (or the
# owner has hand-edited). Mirrors the old skeleton's copy so the UX intent is unchanged.
_EMPTY_DRAFT_PREVIEW = (
    "_This draft is empty. Once the writer-agent drafts (or you hand-edit and save), "
    "the canonical long-read renders here._"
)

# Greeting shown once at the top of every editor chat. Names the hard rule the owner relies on:
# edits apply in place and manual hand-edits survive.
_CHAT_INTRO = (
    "Chat with the editor to refine this draft. Edits apply in place — your manual edits to the "
    "draft (saved on the right) are preserved."
)


# --- DB session helper ---------------------------------------------------------------------


@contextmanager
def _db_session() -> Iterator:
    """Yield a short-lived DB Session, always closed on exit (success AND exception).

    Each page render / action opens its own session and closes it promptly — there is one owner,
    no concurrency, so a per-action session is simplest and avoids holding a connection across the
    page's lifetime. `get_session` is imported lazily so importing this module never constructs
    the engine or touches the DB (uvicorn boot, test collection stay side-effect-free)."""
    from app.db.session import get_session

    session = get_session()
    try:
        yield session
    finally:
        session.close()


# --- page registration ---------------------------------------------------------------------


def register_pages() -> None:
    """Register both NiceGUI pages on the global app. Idempotent at import time via the module
    guard below; exposed as a function so `routes.py` can call it explicitly (and tests can be
    explicit about when registration happens). Decorators run when this is called."""

    @ui.page("/")
    def dashboard_page() -> None:  # noqa: D401 - NiceGUI page function
        _build_dashboard()

    @ui.page("/editor/{article_id}")
    def editor_page(article_id: str) -> None:  # noqa: D401 - NiceGUI page function
        _build_editor(article_id)


# --- page 1: admin / dashboard -------------------------------------------------------------


def _build_dashboard() -> None:
    """Render the admin/dashboard page: a status FILTER over one paginated, unified Stories list.

    A "story" is the pipeline's unit at every stage — an undrafted cluster (Gate-1 new/sent/
    approved/skipped) OR a drafted article/digest (drafting/pre_publish/published) — surfaced by
    `queries.load_stories` as a flat list of `StoryRow`s with an `effective_status` spanning the
    whole STATUS_SPECTRUM. The page is two controls:

      - A status filter ("All" + each status, with its per-status count) — changing it re-queries
        load_stories(status=…) and rebuilds the list in place.
      - One Stories list, paginated CLIENT-SIDE, as a COMPACT table-like row per story (denser than
        a card so many rows fit). Each row shows (left→right, NO score): a status chip, the title
        (single-line, ellipsized), the topic + source-type chips, an "in digest" badge, an "open
        original ↗" link when set, and — RIGHT-ALIGNED — status-aware action buttons.

    Per-row actions depend on the row's `kind` + `effective_status` (Change 1; both already on
    StoryRow): an article/digest gets one "Open" (→ its editor); a new/sent cluster gets "Write →"
    (approve + fetch + draft + open) and "Skip"; an approved cluster gets "Draft →" (fetch + draft +
    open); a skipped cluster gets NO action buttons. This fixes the old bug where every cluster
    showed Draft even when drafting a `new` cluster would raise (create_article_for_cluster requires
    status=='approved' — drafting is only valid after approve+fetch).

    Two filters sit above the list — the status filter and (this slice) a SOURCE filter — and they
    AND together: changing EITHER re-queries load_stories(status=…, source=…) with both current
    selections and rebuilds the list in place ("All" on a filter means None for that axis). The two
    filters' COUNTS are CROSS-FILTERED (dynamic): picking a status re-labels the source toggle with
    source_counts(status=…), and picking a source re-labels the status toggle with
    unified_status_counts(source=…) — so each toggle's counts always reflect the OTHER axis's current
    selection. Both toggles live in a single rebuildable container (`state["_filters_el"]`) that the
    shared filter handler clears+rebuilds with the fresh count labels, preserving each toggle's
    current selection from `state`.

    All reads go through `queries.load_stories` / `queries.unified_status_counts` /
    `queries.source_counts` (SELECT-only). The page mutates state only via the explicit per-row
    pipeline actions (Write/Draft/Skip = Gate-1 + draft writes, coordinated through Postgres) —
    never publishes (hard rule)."""
    _page_header("Dashboard", crumb="stories")

    # Page-local state: the active status + source filters (None = "All" on each axis) and the elements
    # the filter handlers rebuild. NiceGUI gives each browser session its own page invocation, so this
    # dict is page-local. The two filters AND together when load_stories is re-queried, and their counts
    # cross-filter (each toggle's labels reflect the OTHER axis's current selection).
    state: dict = {"status": None, "source": None}

    with ui.column().classes("w-full max-w-5xl mx-auto p-4 gap-4").mark("dashboard"):
        # Flagship intake (Phase 10): the "New piece from my material" entry point sits above the
        # filters — it mints a cluster-less article grounded on the owner's OWN material (pasted
        # text / an uploaded file / a fetched URL), drafts it, and opens its editor. Distinct from
        # the per-row Write/Draft, which start from an approved CLUSTER.
        _build_new_piece_entry(state)

        # Both filter toggles live in this container so the shared handler can clear+rebuild them with
        # fresh (cross-filtered) count labels while preserving each toggle's current selection.
        filters_el = ui.column().classes("w-full gap-2").mark("filters")
        state["_filters_el"] = filters_el
        _build_filters(state)

        list_el = ui.column().classes("w-full gap-1").mark("stories-list")
        state["_list_el"] = list_el
        _render_stories(state)


# --- flagship intake: "New piece from my material" (own-material → canonical draft) ----------
#
# Phase 10. The owner's OWN material — pasted notes, an uploaded file (md/txt/log/.ipynb), or a
# source URL — becomes the grounding for a cluster-less FLAGSHIP article that the writer-agent
# drafts. This is the third way a draft is born (alongside Write/Draft on an approved cluster):
# `create_flagship_article` mints the article, `attach_owner_source`/`attach_owner_url`/
# `parse_uploaded_file` store the grounding corpus, `draft_article` runs the agent, then we open
# its editor. It never posts (hard rule) — it only produces a draft for the owner to iterate.
#
# The SAME intake form (text / file / url) is reused on the editor page's "Attach material"
# control, so the inputs + the file-capture wiring live in one shared helper (`_build_intake_form`)
# keyed by a mark-prefix ("new-piece" on the dashboard, "attach" on the editor).


def _build_new_piece_entry(state: dict) -> None:
    """Render the dashboard's "New piece from my material" button + its intake dialog (Phase 10).

    The button (`.mark("new-piece-button")`) opens a dialog (`.mark("new-piece-dialog")`) holding
    the shared intake form (a piece-type select, a pasted-text area, a file upload, and a source
    URL) plus a "Create & draft" submit (`.mark("new-piece-submit")`). Submit mints a flagship
    article, attaches whatever material the owner supplied, runs the writer-agent draft, and
    navigates into the new editor — all off the event loop behind a spinner.

    The dialog also carries the Phase-10b "Find related news" control (`.mark("new-piece-find-
    related")`) — READ-ONLY discovery here (the article doesn't exist yet), so the results just list
    related news with open-original links and no attach button (`fusion_attach=None`).

    The form elements + the captured upload bytes live in a per-dialog `form` dict so the submit
    handler can read them; the dialog is stashed so submit can close it on success."""
    from app.editor.article import PIECE_TYPES

    dialog, form = _build_intake_dialog(
        mark_prefix="new-piece",
        title="New piece from my material",
        submit_label="Create & draft",
        piece_types=PIECE_TYPES,
        default_piece_type=_FLAGSHIP_DEFAULT_PIECE_TYPE,
        on_submit=lambda: _on_new_piece_submit(state, form, dialog),
    )

    ui.button("New piece from my material", icon="edit_note", on_click=dialog.open).props(
        "color=primary unelevated"
    ).classes("self-start").mark("new-piece-button")


# The flagship default piece type — the teach-down explainer the flagship flow targets. Mirrors
# app.editor.sources.DEFAULT_FLAGSHIP_PIECE_TYPE; kept as a local constant so the UI's default
# select value is a plain literal (it is validated against PIECE_TYPES at construction time).
_FLAGSHIP_DEFAULT_PIECE_TYPE = "tech_explainer"


def _build_intake_dialog(
    *,
    mark_prefix: str,
    title: str,
    submit_label: str,
    piece_types,
    default_piece_type: str | None,
    on_submit: Callable,
    fusion_attach: tuple | None = None,
):
    """Build a `ui.dialog` holding the shared owner-material intake form; return (dialog, form).

    The form is the same on both surfaces: a pasted-text area, a file upload (md/txt/log/.ipynb),
    and a source URL — and, ONLY when `piece_types` is given (the dashboard "new piece" path), a
    piece-type select (the editor "attach material" path has no piece-type select; the article
    already has a type). `form` is a dict the submit handler reads:
      - "piece_type_el" (or None), "text_el", "url_el" — the input elements.
      - "upload" — the captured {"name", "data"} of the last uploaded file (set by the upload
        handler), or None.
      - "submit_btn" — the submit button (so the handler can disable it while working).
      - "fusion_results_el" — the results container the Find-related handler rebuilds (Phase 10b).

    The form ALSO carries the Phase-10b "Find related news" fusion control: a button that embeds the
    pasted text and lists the existing news clusters most related to it (discovery — "what news
    connects to my material"). On the dashboard new-piece dialog it is READ-ONLY (the article doesn't
    exist yet); on the editor attach-material dialog (`fusion_attach=(article_id, state)`) each result
    also gets an "Attach as source" button that pulls that cluster's source URL into the open article
    (the FUSION path) — it never creates an article_clusters link.

    The submit handler (`on_submit`, an async callable) is wired to the submit button; it owns the
    create/attach/draft (or attach-only) chain and closes/refreshes as appropriate."""
    form: dict = {"upload": None}
    with ui.dialog().mark(f"{mark_prefix}-dialog") as dialog:
        with ui.card().classes("w-full max-w-xl gap-3 p-4"):
            ui.label(title).classes("text-base font-semibold")
            ui.label(
                "Ground the draft in your OWN material — paste notes, upload a file, or give a "
                "source URL. At least one is required. Nothing is ever posted."
            ).classes("text-xs text-gray-500")

            if piece_types is not None:
                form["piece_type_el"] = (
                    ui.select(
                        list(piece_types),
                        value=(
                            default_piece_type
                            if default_piece_type in piece_types
                            else None
                        ),
                        label="Piece type",
                    )
                    .props("outlined dense options-dense")
                    .classes("w-full")
                    .mark(f"{mark_prefix}-piece-type")
                )
            else:
                form["piece_type_el"] = None

            form["text_el"] = (
                ui.textarea(label="Pasted text / notes")
                .props("outlined autogrow")
                .classes("w-full")
                .mark(f"{mark_prefix}-text")
            )

            ui.label("File (md / txt / log / .ipynb)").classes(
                "text-xs uppercase tracking-wide text-gray-500"
            )

            async def _on_file_upload(e) -> None:
                # Capture the uploaded file's bytes + name into the form dict (read off the event
                # loop where NiceGUI's FileUpload.read is async). auto_upload fires this on select.
                data = await e.file.read()
                form["upload"] = {"name": e.file.name, "data": data}
                ui.notify(f"Attached file: {e.file.name}", type="positive")

            (
                ui.upload(on_upload=_on_file_upload, auto_upload=True)
                .props('accept=".md,.markdown,.txt,.log,.ipynb"')
                .classes("w-full")
                .mark(f"{mark_prefix}-upload")
            )

            form["url_el"] = (
                ui.input(label="Source URL")
                .props("outlined dense")
                .classes("w-full")
                .mark(f"{mark_prefix}-url")
            )

            # Phase 10b — the "Find related news" fusion-discovery control over the pasted text.
            _build_fusion_section(mark_prefix, form, fusion_attach)

            with ui.row().classes("w-full justify-end gap-2"):
                ui.button("Cancel", on_click=dialog.close).props("flat color=grey")
                form["submit_btn"] = (
                    ui.button(submit_label, on_click=on_submit)
                    .props("color=primary unelevated")
                    .mark(f"{mark_prefix}-submit")
                )
    return dialog, form


# --- fusion discovery: "Find related news" over the owner's material (Phase 10b) ------------
#
# Embeds the pasted text and lists the existing news clusters most related to it via
# `app.editor.find_related_clusters` (deterministic: one embed + a pgvector query). On the dashboard
# new-piece dialog this is pure DISCOVERY ("what news connects to my material") before the article
# exists — read-only. On the editor attach-material dialog it is the FUSION path: each result gets an
# "Attach as source" button that pulls that cluster's source URL into the OPEN article via
# `attach_owner_url` (NO article_clusters link — the covered-marker stays untouched). Never posts.


def _build_fusion_section(mark_prefix: str, form: dict, fusion_attach: tuple | None) -> None:
    """Render the "Find related news" button + the results container inside the intake dialog.

    The button (`.mark(f"{mark_prefix}-find-related")`) runs the fusion query over the pasted text;
    the results render into `form["fusion_results_el"]` (`.mark("related-results")`). When
    `fusion_attach` is `(article_id, state)` the results are attachable (each gets an "Attach as
    source" button); when it is None the results are read-only discovery."""
    with ui.row().classes("w-full items-center gap-2"):
        ui.button(
            "Find related news",
            icon="travel_explore",
            on_click=lambda: _on_find_related_click(mark_prefix, form, fusion_attach),
        ).props("flat dense color=primary").mark(f"{mark_prefix}-find-related")
        ui.label("Discover existing news related to your material.").classes(
            "text-xs text-gray-500"
        )
    form["fusion_results_el"] = (
        ui.column().classes("w-full gap-1").mark("related-results")
    )


async def _on_find_related_click(
    mark_prefix: str, form: dict, fusion_attach: tuple | None
) -> None:
    """Handle a "Find related news" click: embed the pasted text, query related clusters off the
    event loop, and render them into the results container (Phase 10b).

    Empty input → a notify and NO backend call (nothing to embed). On return, the results container is
    rebuilt: a "no related news found" line for an empty result, else one row per related cluster
    (title, a topic chip + source-type chips, an "open original ↗" link when the cluster has a URL,
    and — on the editor attach path — an "Attach as source" button). A backend `ValueError` surfaces
    as a negative notify. Read-only discovery on the dashboard; the fusion attach path on the editor."""
    text_el = form.get("text_el")
    text = ((text_el.value if text_el is not None else "") or "").strip()
    results_el = form.get("fusion_results_el")
    if not text:
        ui.notify(
            "Paste some text first — Find related news searches over your material.",
            type="negative",
        )
        return

    progress = ui.notification("Finding related news…", spinner=True, timeout=None)
    try:
        results = await run.io_bound(_find_related, text)
    except ValueError as e:
        progress.dismiss()
        ui.notify(str(e), type="negative", multi_line=True, close_button="Dismiss")
        return
    except Exception as e:  # pragma: no cover - defensive; surfaces unexpected failures
        progress.dismiss()
        log.exception("find-related failed")
        ui.notify(
            f"Find related failed: {type(e).__name__}: {e}", type="negative", multi_line=True
        )
        return
    progress.dismiss()
    if results_el is not None:
        _render_related_results(results_el, results, fusion_attach)


def _find_related(text: str) -> list:
    """Blocking core of "Find related news" (runs in a worker thread via run.io_bound). Opens its own
    short-lived session and calls `find_related_clusters`, which embeds the text once and pgvector-
    searches the dedup index, returning a list[RelatedCluster] (detached primitives). app.editor is
    imported lazily so this module's import never pulls the embedding stack. SELECT-only — never
    writes, never posts."""
    from app.editor import find_related_clusters

    with _db_session() as session:
        return find_related_clusters(session, text)


def _render_related_results(
    results_el, results: list, fusion_attach: tuple | None
) -> None:
    """Populate the related-results container with one row per related cluster (or a "no related news
    found" line). Cleared and rebuilt in place.

    Each row shows the cluster title, a topic chip, its source-type chips, and an "open original ↗"
    link (new tab) when the cluster has a URL. On the editor attach path (`fusion_attach=(article_id,
    state)`) the row also gets an "Attach as source" button (`.mark(f"attach-related-{i}")`) that
    pulls that cluster's URL into the open article via `attach_owner_url` (disabled when the cluster
    has no URL — nothing to fetch). Read-only on the dashboard discovery path."""
    results_el.clear()
    with results_el:
        if not results:
            ui.label("No related news found.").classes(
                "text-xs italic text-gray-500"
            ).mark("related-empty")
            return
        for i, rc in enumerate(results):
            _render_related_row(i, rc, fusion_attach)


def _render_related_row(index: int, rc, fusion_attach: tuple | None) -> None:
    """One related-cluster row: title + a topic chip + source-type chips + an open-original link, and
    — on the editor attach path — an "Attach as source" button. `rc` is a detached
    `app.editor.RelatedCluster` (primitives only)."""
    with ui.card().classes("w-full gap-1 p-2").mark(f"related-row-{index}"):
        with ui.row().classes("w-full items-center gap-2 no-wrap"):
            ui.label(rc.title or "(untitled)").classes("grow text-sm truncate").tooltip(
                rc.title or "(untitled)"
            )
            if rc.url:
                ui.link("open original ↗", rc.url, new_tab=True).classes(
                    "text-primary text-xs no-underline whitespace-nowrap"
                ).mark(f"related-open-{index}")
        with ui.row().classes("w-full items-center gap-1 no-wrap"):
            ui.badge(rc.topic or "—").props("color=grey-7").classes(
                "text-xs whitespace-nowrap"
            )
            for src in rc.source_types or []:
                ui.badge(src).props(f"color={_source_chip_color(src)}").classes(
                    "text-xs whitespace-nowrap"
                )
            if fusion_attach is not None:
                article_id, state = fusion_attach
                attach_btn = (
                    ui.button(
                        "Attach as source",
                        on_click=lambda u=rc.url: _on_attach_related_click(
                            article_id, state, u
                        ),
                    )
                    .props("flat dense color=primary")
                    .classes("ml-auto")
                    .mark(f"attach-related-{index}")
                )
                if not rc.url:
                    # No URL to fetch — there is nothing to attach as a grounding source.
                    attach_btn.disable()


async def _on_attach_related_click(article_id: str, state: dict, url: str | None) -> None:
    """Handle an "Attach as source" click on a related-cluster row (the FUSION path, Phase 10b):
    fetch the cluster's URL and attach its text as an owner grounding source on the OPEN article, off
    the event loop, then refresh the Sources panel.

    This goes through `attach_owner_url` (which fetches + stores the text as an owner source) — it does
    NOT create an article_clusters link, so the cluster's covered-marker stays untouched (a related
    news source joins the piece without the cluster being consumed). A None/blank URL is a no-op guard
    (the button is disabled in that case). A backend `ValueError` (e.g. the fetch yielded nothing)
    surfaces as a negative notify. Never posts."""
    if not (url or "").strip():
        ui.notify("This related item has no URL to attach.", type="negative")
        return
    progress = ui.notification("Attaching related news as a source…", spinner=True, timeout=None)
    try:
        await run.io_bound(_attach_related_url, article_id, url)
    except ValueError as e:
        progress.dismiss()
        log.info("attach-related refused for article %s: %s", article_id, e)
        ui.notify(str(e), type="negative", multi_line=True, close_button="Dismiss")
        return
    except Exception as e:  # pragma: no cover - defensive; surfaces unexpected failures
        progress.dismiss()
        log.exception("attach-related failed for article %s", article_id)
        ui.notify(
            f"Attach failed: {type(e).__name__}: {e}", type="negative", multi_line=True
        )
        return
    progress.dismiss()
    _refresh_sources(article_id, state)
    ui.notify("Related news attached as a source", type="positive")


def _attach_related_url(article_id: str, url: str) -> int:
    """Blocking core of "Attach as source" (runs in a worker thread via run.io_bound). Opens its own
    short-lived session and calls `attach_owner_url`, which fetches the URL's text and stores it as an
    owner grounding source (NO article_clusters link). app.editor is imported lazily so this module's
    import never pulls the fetcher stack. Postgres-only write — never posts."""
    from app.editor import attach_owner_url

    with _db_session() as session:
        return attach_owner_url(session, article_id, url)


def _intake_inputs(form: dict) -> tuple[str, dict | None, str]:
    """Read the three raw intake inputs from a form dict: (text, upload-or-None, url).

    Strips the text and URL; the upload is the captured {"name","data"} (or None). Centralised so
    the new-piece and attach-material handlers read the form identically."""
    text_el = form.get("text_el")
    url_el = form.get("url_el")
    text = ((text_el.value if text_el is not None else "") or "").strip()
    url = ((url_el.value if url_el is not None else "") or "").strip()
    upload = form.get("upload")
    return text, upload, url


async def _on_new_piece_submit(state: dict, form: dict, dialog) -> None:
    """Handle "Create & draft": mint a flagship article from the owner's material, draft it, and
    open its editor (Phase 10). Runs the whole create→attach→draft chain off the event loop.

    Validation: at least one of pasted text / an uploaded file / a URL must be present; otherwise a
    negative notify and the dialog stays open (nothing is created). The selected piece type defaults
    to tech_explainer. A URL fetch that yields nothing is tolerated WHEN there is other material
    (the article + the other sources still proceed, with a notify); if the URL was the ONLY input
    and it failed, the whole submit is surfaced as an error (nothing usable was grounded). Any
    backend ValueError surfaces as a negative notify without crashing the page. On success we close
    the dialog and navigate to /editor/<new id>."""
    text, upload, url = _intake_inputs(form)
    if not (text or upload or url):
        ui.notify(
            "Add at least one of: pasted text, an uploaded file, or a source URL.",
            type="negative",
        )
        return

    piece_el = form.get("piece_type_el")
    piece_type = (piece_el.value if piece_el is not None else None) or _FLAGSHIP_DEFAULT_PIECE_TYPE

    submit_btn = form.get("submit_btn")
    if submit_btn is not None:
        submit_btn.disable()
    progress = ui.notification(
        "Creating the piece and running the writer-agent…", spinner=True, timeout=None
    )
    try:
        article_id, url_failed = await run.io_bound(
            _create_flagship_and_draft, piece_type, text, upload, url
        )
    except ValueError as e:
        progress.dismiss()
        if submit_btn is not None:
            submit_btn.enable()
        log.info("new-piece submit refused: %s", e)
        ui.notify(str(e), type="negative", multi_line=True, close_button="Dismiss")
        return
    except Exception as e:  # pragma: no cover - defensive; surfaces unexpected failures
        progress.dismiss()
        if submit_btn is not None:
            submit_btn.enable()
        log.exception("new-piece submit failed")
        ui.notify(
            f"Create failed: {type(e).__name__}: {e}", type="negative", multi_line=True
        )
        return
    progress.dismiss()
    if url_failed:
        # The URL yielded nothing but other material grounded the draft — surface it so the owner
        # knows that source was skipped (the piece was still created from the rest).
        ui.notify(
            "Could not fetch the URL — created the piece from your other material.",
            type="warning",
            multi_line=True,
        )
    dialog.close()
    ui.navigate.to(f"/editor/{article_id}")


def _create_flagship_and_draft(
    piece_type: str, text: str, upload: dict | None, url: str
) -> tuple[str, bool]:
    """Blocking core of "Create & draft" (runs in a worker thread via run.io_bound). Returns
    (article_id, url_failed) — url_failed is True when a URL was given, yielded nothing, but other
    material grounded the draft (so the handler can warn the owner that source was skipped).

    Opens its own session and runs the flagship chain:
      1. create_flagship_article(piece_type) — mint the cluster-less article.
      2. attach the supplied material in order — pasted text, then the uploaded file (parsed to
         text via parse_uploaded_file), then the URL (fetched via attach_owner_url).
      3. draft_article — run the writer-agent over the attached material.
    A URL fetch failure is tolerated when OTHER material was attached (we skip it and let the draft
    proceed on the rest); if the URL was the ONLY material, its ValueError propagates so the handler
    surfaces it (nothing usable to ground on). app.editor is imported lazily. Postgres-only writes —
    never posts."""
    from app.editor import (
        attach_owner_source,
        attach_owner_url,
        create_flagship_article,
        draft_article,
        parse_uploaded_file,
    )

    with _db_session() as session:
        article_id = create_flagship_article(session, piece_type=piece_type)
        attached_any = False
        url_failed = False
        if text:
            attach_owner_source(
                session, article_id, kind="text", content=text, title="Pasted note"
            )
            attached_any = True
        if upload is not None:
            content = parse_uploaded_file(upload["name"], upload["data"])
            attach_owner_source(
                session, article_id, kind="file", title=upload["name"], content=content
            )
            attached_any = True
        if url:
            try:
                attach_owner_url(session, article_id, url)
                attached_any = True
            except ValueError:
                if not attached_any:
                    # The URL was the only input and it yielded nothing — fail loudly so the owner
                    # knows to paste the text instead (the message names the cause).
                    raise
                url_failed = True
                log.info(
                    "flagship %s: url fetch yielded nothing, proceeding on other material",
                    article_id,
                )
        draft_article(session, article_id)
        return article_id, url_failed


# How many story rows render per page in the client-side paginator. Sized generously (a single
# owner browses, not searches) while keeping the DOM bounded — the list is paginated so even a
# large backlog never dumps every row at once.
_STORIES_PER_PAGE = 25

# The shared CSS grid-template-columns for the Stories TABLE (Variant 1). The HEADER row and every
# story row use this EXACT template so the four columns line up into clean vertical lanes the eye
# can run down:
#   col 1 — status chip      (fixed ~92px so every chip sits in the same lane)
#   col 2 — title            (1fr + min-width:0 so it takes the slack and can ellipsize-truncate)
#   col 3 — meta             (auto: topic + source chips + in-digest badge + open-original link)
#   col 4 — actions          (auto: the status-aware buttons, right-aligned)
# Applied via an inline `display:grid` style (Tailwind has no arbitrary grid-template util wired in
# here), kept identical on header + rows by referencing this one constant.
_STORIES_GRID_STYLE = (
    "display:grid;"
    "grid-template-columns:92px minmax(0,1fr) auto auto;"
    "align-items:center;"
    "column-gap:12px;"
)


def _build_filters(state: dict) -> None:
    """Build (or rebuild) BOTH filter toggles — status and source — inside the rebuildable container
    `state["_filters_el"]`, with CROSS-FILTERED count labels.

    This is the heart of the dynamic-counts behavior. It reads, in one shot:
      - the SOURCE counts cross-filtered by the current status — `source_counts(status=state["status"])`
      - the STATUS counts cross-filtered by the current source — `unified_status_counts(source=state["source"])`
    then clears the container and rebuilds each toggle so its labels carry those fresh counts. Each
    toggle is constructed with its CURRENT selection (`state["status"]` / `state["source"]`, mapped to
    the `_ALL_FILTER` sentinel for None) as its value, so a rebuild PRESERVES which option is
    highlighted. So picking status="sent" makes every source count show (0); picking source="arxiv"
    re-labels the status counts to arxiv-only.

    Called once at page build, then again by each filter's change handler (after it has set its axis
    on `state`) so BOTH toggles AND the list refresh together on either change."""
    status_counts = _load_status_counts(state["source"])
    source_counts = _load_source_counts(state["status"])
    # The source filter's "All" = the total number of stories matching the current STATUS filter
    # (any source). Source counts are multi-valued (a story has 0+ source types, digests have none),
    # so their sum is NOT the story total — count the matching stories directly so "All" matches what
    # clicking it actually shows (and lines up with the status filter's "All").
    source_all = len(_load_stories(state["status"], None))

    filters_el = state["_filters_el"]
    filters_el.clear()
    with filters_el:
        _build_status_filter(state, status_counts)
        _build_source_filter(state, source_counts, source_all)


def _build_status_filter(state: dict, counts: dict) -> None:
    """The status filter: a `ui.toggle` of "All" + each STATUS_SPECTRUM status, each option labelled
    with its per-status count from `unified_status_counts(source=…)` (cross-filtered by the current
    source selection). Changing it sets `state["status"]` (None for "All") and rebuilds BOTH filter
    toggles (fresh cross-filtered counts) AND the Stories list in place.

    Marked `.mark("status-filter")`. The toggle VALUE is the raw status string (or the sentinel
    "__all__" for All) so the handler maps cleanly to the load_stories(status=…) arg; the visible
    LABEL carries the count so the owner sees the distribution at a glance. Constructed with the
    CURRENT selection as its value so a container rebuild preserves the highlighted option."""
    total = sum(counts.values())
    options = {_ALL_FILTER: f"All ({total})"}
    for status in queries.STATUS_SPECTRUM:
        options[status] = f"{status} ({counts.get(status, 0)})"

    current = state["status"] if state["status"] is not None else _ALL_FILTER
    toggle = (
        ui.toggle(options, value=current)
        .props("no-caps dense")
        .classes("flex-wrap")
        .mark("status-filter")
    )

    def _on_filter_change(e) -> None:
        # Sync handler on purpose: the rebuild is a fast SELECT + a UI build (no await), and a
        # programmatic value-change only dispatches a SYNCHRONOUS on_value_change in the test client
        # (an async one is dropped). Keeping it sync makes the filter testable and is correct for the
        # single owner — there is no blocking work to push off the event loop here.
        state["status"] = None if e.value == _ALL_FILTER else e.value
        _build_filters(state)  # re-label BOTH toggles with fresh cross-filtered counts
        _render_stories(state)

    toggle.on_value_change(_on_filter_change)


def _build_source_filter(state: dict, counts: dict, all_total: int) -> None:
    """The source filter: a `ui.toggle` of "All" + each source-type present in the story set, each
    option labelled with its count from `queries.source_counts(status=…)` (cross-filtered by the
    current status selection). Mirrors the status filter exactly — changing it sets `state["source"]`
    (None for "All") and rebuilds BOTH filter toggles (fresh cross-filtered counts) AND the Stories
    list in place, ANDed with the current status selection.

    Marked `.mark("source-filter")` and placed just below the status filter. The toggle VALUE is the
    raw source-type string (e.g. "rss", "hn", "arxiv", "x_user", "github" — the sentinel `_ALL_FILTER`
    for All), so the handler maps cleanly to the load_stories(source=…) arg; the visible LABEL carries
    the count so the owner sees the source distribution at a glance (e.g. "rss (120)"). Source types
    come from config and vary, so there is no fixed universe — the options are exactly the source
    types `source_counts` reports, in a stable alphabetical order. Constructed with the CURRENT
    selection as its value so a container rebuild preserves the highlighted option."""
    options = {_ALL_FILTER: f"All ({all_total})"}
    # Stable, owner-friendly order: source types alphabetically.
    for source in sorted(counts):
        options[source] = f"{source} ({counts[source]})"

    current = state["source"] if state["source"] is not None else _ALL_FILTER
    toggle = (
        ui.toggle(options, value=current)
        .props("no-caps dense")
        .classes("flex-wrap")
        .mark("source-filter")
    )

    def _on_filter_change(e) -> None:
        # Sync handler, same rationale as the status filter: the rebuild is a fast SELECT + a UI build
        # (no await), and a programmatic value-change only dispatches a SYNCHRONOUS on_value_change in
        # the test client. Setting state["source"] then rebuilding re-queries load_stories with BOTH
        # axes (status AND source) and re-labels both toggles with fresh cross-filtered counts.
        state["source"] = None if e.value == _ALL_FILTER else e.value
        _build_filters(state)  # re-label BOTH toggles with fresh cross-filtered counts
        _render_stories(state)

    toggle.on_value_change(_on_filter_change)


# Sentinel toggle value for the "All" (no-filter) option — kept distinct from any real status so
# the handler can map it to `status=None` without colliding with a status named "all".
_ALL_FILTER = "__all__"


def _load_status_counts(source: str | None) -> dict:
    """The per-status story counts for the status-filter labels: {status: n} across STATUS_SPECTRUM,
    CROSS-FILTERED by the current source — `queries.unified_status_counts(source=…)` (SELECT-only).
    `source=None` counts over every story; `source=S` counts only stories carrying source-type S, so
    the status labels reflect the source filter the owner has selected. Degrades to an empty dict on a
    read hiccup (the labels just show 0) rather than blanking the page — the filter still works."""
    try:
        with _db_session() as session:
            return queries.unified_status_counts(session, source=source)
    except Exception:  # pragma: no cover - defensive; the filter degrades to zero counts
        log.exception("loading unified status counts failed (source=%r)", source)
        return {}


def _load_source_counts(status: str | None) -> dict:
    """The per-source-type story counts for the source-filter labels: {source_type: n}, keys exactly
    as they appear on StoryRow ("rss", "hn", "arxiv", "x_user", "github", …), CROSS-FILTERED by the
    current status — `queries.source_counts(status=…)` (SELECT-only). `status=None` counts over every
    story; `status=X` counts only stories whose effective_status == X, so the source labels reflect the
    status filter the owner has selected (a status with no stories makes every source count 0).
    Multi-valued (a story counts toward each of its source types), so the counts need not sum to the
    story total. Degrades to an empty dict on a read hiccup (the source filter then shows only
    "All (0)") rather than blanking the page."""
    try:
        with _db_session() as session:
            return queries.source_counts(session, status=status)
    except Exception:  # pragma: no cover - defensive; the filter degrades to zero counts
        log.exception("loading source counts failed (status=%r)", status)
        return {}


def _load_stories(status: str | None, source: str | None) -> list:
    """The story rows for the current filters: `queries.load_stories(session, status=…, source=…)`
    (SELECT-only). The two filters AND together — `None` on an axis means "no filter on that axis";
    `source=S` keeps only rows whose source_types contains S. Opens its own short-lived session.
    Degrades to [] on a read hiccup (rendered as the muted "No stories." note) so a query failure
    can't blank the dashboard."""
    try:
        with _db_session() as session:
            return queries.load_stories(session, status=status, source=source)
    except Exception:  # pragma: no cover - defensive; the list degrades to the empty note
        log.exception("loading stories failed (status=%r, source=%r)", status, source)
        return []


def _render_stories(state: dict) -> None:
    """Rebuild the Stories TABLE in place from a fresh `load_stories(status=state["status"],
    source=state["source"])` read — the status and source filters AND together.

    Clears the container, then renders the Variant-1 table: a faint HEADER ROW of muted column
    labels, then a CLIENT-SIDE paginated body — the rows are sliced per page and a `ui.pagination`
    control flips the visible page without a server round-trip (one owner, the whole filtered set is
    already in memory). Header + every row share `_STORIES_GRID_STYLE` so the four columns line up
    into clean vertical lanes. An empty result shows a muted "No stories." note (no header)."""
    list_el = state.get("_list_el")
    if list_el is None:
        return
    stories = _load_stories(state["status"], state.get("source"))

    list_el.clear()
    with list_el:
        if not stories:
            ui.label("No stories.").classes("italic text-gray-500").mark("stories-empty")
            return

        _stories_header_row()

        n_pages = (len(stories) + _STORIES_PER_PAGE - 1) // _STORIES_PER_PAGE
        # The page-local current page (1-based). A fresh render (filter change) resets to page 1.
        page_state = {"page": 1}
        rows_box = ui.column().classes("w-full gap-0")

        def _render_page() -> None:
            rows_box.clear()
            start = (page_state["page"] - 1) * _STORIES_PER_PAGE
            with rows_box:
                for story in stories[start : start + _STORIES_PER_PAGE]:
                    _story_row(state, story)

        if n_pages > 1:
            def _on_page_change(e) -> None:
                page_state["page"] = e.value
                _render_page()

            ui.pagination(1, n_pages, value=1, direction_links=True).on_value_change(
                _on_page_change
            ).classes("self-center mt-2").mark("stories-pagination")

        _render_page()


def _stories_header_row() -> None:
    """The faint header row above the table: muted column labels aligned to the SAME grid as every
    story row (`_STORIES_GRID_STYLE`), so "статус / історія / джерело / (actions)" sit directly atop
    their columns. Ukrainian sentence-case labels match the rest of the app; 11px + a tertiary text
    colour keep it a quiet column guide, not a heavy table chrome. The 4th column header is blank
    (the actions column needs no label)."""
    with ui.element("div").classes("w-full px-3 py-1").style(_STORIES_GRID_STYLE).mark(
        "stories-header"
    ):
        for label in ("статус", "історія", "джерело", ""):
            ui.label(label).style(
                "font-size:11px;color:var(--color-text-tertiary,#9ca3af);"
                "text-transform:none;white-space:nowrap;"
            )


def _story_row(state: dict, story) -> None:
    """One story row of the Variant-1 TABLE — a CSS grid whose four columns line up with the header
    (both use `_STORIES_GRID_STYLE`). `story` is a `queries.StoryRow` (detached primitives).

    The row is exactly FOUR grid children, left→right (NO score/ratio anywhere — that ranking detail
    is deliberately absent from this owner-facing list):
      col 1 — the status CHIP (colour by status, fixed ~92px lane so chips align down the column).
      col 2 — the TITLE on a SINGLE line, truncated with an ellipsis (overflow hidden / nowrap) so a
              long owner title can't blow the row height; a tooltip carries the full title.
      col 3 — the META group, right-grouped: the topic + source-type chips, the "in digest" badge,
              and the "open original ↗" link, in one tight no-wrap horizontal row.
      col 4 — the ACTIONS group, right-aligned: the status-aware buttons.

    Vertically centred, dense padding (~8–9px), a 0.5px bottom divider, and a subtle hover tint keep
    the rows scannable as a clean table. The actions are STATUS-AWARE (Change 1) via `_row_actions`:
    article/digest → Open; new/sent cluster → Write → + Skip; approved cluster → Draft →; skipped →
    none. Buttons/chips/link keep their original per-key/per-cluster marks so tests still target them.
    """
    with ui.element("div").classes("w-full hover:bg-gray-50").style(
        _STORIES_GRID_STYLE
        + "padding:8px 12px;border-bottom:0.5px solid var(--color-border-tertiary,#e5e7eb);"
    ).mark(f"story-{story.key}"):
        # col 1 — status chip. Fixed lane (col width) so every chip aligns into one column;
        # justify-self:start keeps the chip hugging its text instead of stretching the lane.
        ui.badge(story.effective_status).props(
            f"color={_status_color(story.effective_status)}"
        ).classes("text-xs whitespace-nowrap").style("justify-self:start;")

        # col 2 — title: single line, ellipsis-truncated, full title in a tooltip.
        ui.label(story.title or "(untitled)").classes("font-medium").style(
            "min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"
        ).tooltip(story.title or "(untitled)")

        # col 3 — meta group: topic + source chips + in-digest badge + open-original link, in one
        # tight no-wrap horizontal lane pushed to the right edge of its column.
        with ui.row().classes("items-center gap-1 no-wrap justify-end"):
            ui.badge(story.topic or "—").props("color=grey-7").classes(
                "text-xs whitespace-nowrap"
            )
            for src in story.source_types or []:
                ui.badge(src).props(f"color={_source_chip_color(src)}").classes(
                    "text-xs whitespace-nowrap"
                ).mark(f"src-{story.key}-{src}")
            if story.in_digest:
                ui.badge("in digest").props("color=purple-5").classes(
                    "text-xs whitespace-nowrap"
                ).mark(f"in-digest-{story.key}")
            if story.original_url:
                ui.link("open original ↗", story.original_url, new_tab=True).classes(
                    "text-primary text-xs no-underline whitespace-nowrap"
                ).mark(f"open-original-{story.key}")

        # col 4 — right-aligned, status-aware actions (Change 1).
        with ui.row().classes("items-center gap-1 no-wrap justify-end"):
            _row_actions(state, story)


def _row_actions(state: dict, story) -> None:
    """The status-aware, right-aligned action buttons for one story row (Change 1).

    The button set depends on the row's `kind` + `effective_status` (both already on StoryRow) — this
    fixes the old always-on Approve/Skip/Draft, where Draft on a `new` cluster called
    create_article_for_cluster (which requires status=='approved') and raised. The matrix:

      - article / digest                       → Open (→ its editor).
      - cluster, new/sent                       → Write → (approve+fetch+draft+open) + Skip.
      - cluster, approved                       → Draft → (fetch+draft+open; the cluster is already
                                                  green-lit, so no Skip).
      - cluster, skipped (or any other status)  → no action buttons (the status chip + open-original
                                                  link already tell the story).

    Write/Draft/Skip are pipeline writes coordinated through Postgres (Write/Draft run the real
    writer-agent off the event loop behind a spinner); none ever posts (hard rule)."""
    if story.kind in ("article", "digest"):
        ui.button(
            "Open",
            on_click=lambda a=story.article_id: ui.navigate.to(f"/editor/{a}"),
        ).props("color=primary unelevated dense").mark(f"open-{story.key}")
        return

    # kind == "cluster": branch on the Gate-1 / draft status.
    cid = story.cluster_id
    status = story.effective_status
    if status in ("new", "sent"):
        ui.button(
            "Write →",
            on_click=lambda c=cid: _on_write_click(state, c),
        ).props("color=primary unelevated dense").mark(f"write-{cid}")
        ui.button(
            "Skip",
            on_click=lambda c=cid: _on_skip_cluster_click(state, c),
        ).props("color=grey unelevated dense").mark(f"skip-{cid}")
    elif status == "approved":
        ui.button(
            "Draft →",
            on_click=lambda c=cid: _on_draft_click(c),
        ).props("color=primary unelevated dense").mark(f"draft-{cid}")
    # status == "skipped" (or any unexpected value): no action buttons.


# Status → Quasar badge colour for the story chip. Spans the whole STATUS_SPECTRUM so every story,
# at any pipeline stage, reads at a glance across the colour spectrum (new→blue, sent→indigo,
# approved→teal, drafting→amber, pre_publish→purple, published→green, skipped→grey); an unknown
# status falls back to a neutral grey. Quasar colour names (theme-aware, no raw hex) keep the chips
# consistent with the rest of the file and safe in any palette.
_STATUS_COLORS = {
    "new": "blue-4",
    "sent": "indigo-5",
    "approved": "teal-6",
    "skipped": "grey-5",
    "drafting": "amber-7",
    "pre_publish": "purple-6",
    "published": "green-7",
}


def _status_color(status: str) -> str:
    """The Quasar badge colour for a story status (neutral grey for any unknown value)."""
    return _STATUS_COLORS.get(status, "grey-6")


# Source-type → Quasar badge colour for the source chips (the dashboard Stories table + the editor
# Sources panel). The pipeline source types (hn/rss/x_user/github/arxiv) all read as one neutral
# blue-grey lane; the Phase-10 "owner" type — the owner's OWN material, not a third-party source —
# gets a distinct DEEP-PURPLE so a flagship piece's provenance stands out at a glance. Quasar colour
# names (theme-aware, no raw hex) keep it consistent with the rest of the file.
_OWNER_CHIP_COLOR = "deep-purple-5"
_DEFAULT_SOURCE_CHIP_COLOR = "blue-grey-4"


def _source_chip_color(source_type: str) -> str:
    """The Quasar badge colour for a source-type chip — deep-purple for owner material (Phase 10),
    the neutral blue-grey for every pipeline source type."""
    return _OWNER_CHIP_COLOR if source_type == "owner" else _DEFAULT_SOURCE_CHIP_COLOR


# --- Gate-1 + draft actions from the dashboard (Write / Draft / Skip; writes, NEVER posts) ---


async def _on_write_click(state: dict, cluster_id: str) -> None:
    """Handle a "Write →" click on a NEW/SENT cluster: run the whole approve→fetch→create→draft chain
    off the event loop, then navigate into the editor on the fresh draft.

    "Write" collapses Gate-1 approval and the first draft into one owner gesture for an undrafted
    cluster. The chain (one io_bound call) is:
      1. decide(approve=True)        — Gate-1 approve (new/sent → approved); the agreed 2nd Gate-1
                                       surface, reusing the bot's `decide` (coordination via Postgres).
      2. fetch_cluster_full_text     — pass-2 full-text so the writer-agent has source text to ground.
      3. create_article_for_cluster  — mint the `drafting` article + cluster link (needs approved,
                                       which step 1 just set).
      4. draft_article               — run the real writer-agent and persist current_draft.
    On success we navigate to /editor/<article_id>. This is a LONG op (a real writer-agent run), so it
    runs behind a clear "Writing…" spinner. If draft_article raises (the sources yielded no extractable
    text), the article row already exists (it is at `drafting`), so we surface the refusal AND still
    navigate to its editor — the owner can fetch/retry from there. Other ValueErrors (e.g. a stale
    status) surface as a negative notify and stay on the dashboard. Postgres-only writes — never posts."""
    progress = ui.notification(
        "Writing… approving, fetching sources, and running the writer-agent",
        spinner=True,
        timeout=None,
    )
    try:
        article_id = await run.io_bound(_approve_fetch_create_draft, cluster_id)
    except _DraftRefused as e:
        # The article exists (created before draft_article raised); surface the refusal but still
        # open its editor so the owner can act on it.
        progress.dismiss()
        log.info("write: draft refused for cluster %s: %s", cluster_id, e)
        ui.notify(str(e), type="negative", multi_line=True, close_button="Dismiss")
        ui.navigate.to(f"/editor/{e.article_id}")
        return
    except ValueError as e:
        progress.dismiss()
        log.info("write refused for cluster %s: %s", cluster_id, e)
        ui.notify(str(e), type="negative", multi_line=True, close_button="Dismiss")
        return
    except Exception as e:  # pragma: no cover - defensive; surfaces unexpected failures
        progress.dismiss()
        log.exception("write failed for cluster %s", cluster_id)
        ui.notify(f"Write failed: {type(e).__name__}: {e}", type="negative", multi_line=True)
        return
    progress.dismiss()
    ui.navigate.to(f"/editor/{article_id}")


class _DraftRefused(ValueError):
    """A draft_article refusal (e.g. no extractable source text) carrying the already-minted
    article_id, so the Write handler can surface the refusal AND still navigate into the editor for
    that (drafting) article. The article row exists by the time draft_article runs, so opening it is
    acceptable (the spec) — the owner can fetch/retry from the editor."""

    def __init__(self, message: str, article_id: str) -> None:
        super().__init__(message)
        self.article_id = article_id


def _approve_fetch_create_draft(cluster_id: str) -> str:
    """Blocking core of "Write →" (runs in a worker thread via run.io_bound). Opens its own session
    and runs the full chain for a new/sent cluster: Gate-1 approve → pass-2 fetch → create article →
    writer-agent draft, returning the article id. If draft_article raises (sources yielded no
    extractable text) we re-raise as `_DraftRefused` carrying the already-created article id so the
    handler can still open its editor. app.bot.triage / app.fetcher / app.editor are imported lazily
    so this module's import never pulls the bot/fetcher/LLM stacks. Postgres-only writes — never posts."""
    from app.bot.triage import decide
    from app.editor import create_article_for_cluster, draft_article
    from app.fetcher import fetch_cluster_full_text

    with _db_session() as session:
        decide(session, cluster_id, approve=True)
        fetch_cluster_full_text(session, cluster_id)
        article_id = create_article_for_cluster(session, cluster_id)
        try:
            draft_article(session, article_id)
        except ValueError as e:
            raise _DraftRefused(str(e), article_id) from e
        return article_id


async def _on_skip_cluster_click(state: dict, cluster_id: str) -> None:
    """Handle a Skip click on an undrafted cluster: record the Gate-1 skip off the event loop, then
    refresh the list.

    Skip is the same pipeline write the Telegram bot does at Gate 1 — `decide(approve=False)` moves
    the cluster new/sent → skipped. It runs in a worker thread via `run.io_bound`; on success the
    Stories list re-queries so the row moves into the skipped bucket. A ValueError surfaces as a
    negative notify. Postgres-only pipeline write — never posts."""
    progress = ui.notification("Skipping…", spinner=True, timeout=None)
    try:
        await run.io_bound(_skip_cluster, cluster_id)
    except ValueError as e:
        progress.dismiss()
        ui.notify(str(e), type="negative", multi_line=True, close_button="Dismiss")
        return
    except Exception as e:  # pragma: no cover - defensive; surfaces unexpected failures
        progress.dismiss()
        log.exception("skip failed for cluster %s", cluster_id)
        ui.notify(f"Skip failed: {type(e).__name__}: {e}", type="negative", multi_line=True)
        return
    progress.dismiss()
    ui.notify("Skipped", type="positive")
    _render_stories(state)


def _skip_cluster(cluster_id: str) -> None:
    """Blocking core of a dashboard Skip (runs in a worker thread via run.io_bound). Opens its own
    short-lived session and records the Gate-1 skip (`decide(approve=False)`, which commits). app.bot
    .triage is imported lazily. Postgres-only pipeline write — never posts."""
    from app.bot.triage import decide

    with _db_session() as session:
        decide(session, cluster_id, approve=False)


async def _on_draft_click(cluster_id: str) -> None:
    """Handle a "Draft →" click on an APPROVED cluster: run the fetch→create→draft chain off the
    event loop, then navigate to the editor.

    The cluster is already green-lit (Gate-1 approved), so — unlike "Write →" — this chain has NO
    decide step:
      1. fetch_cluster_full_text     — pass-2 full-text (idempotent: a no-op if already fetched) so
                                       the writer-agent has source text to ground.
      2. create_article_for_cluster — mint (or reopen) the `drafting` article + cluster link.
      3. draft_article               — run the writer-agent tool-use loop and persist current_draft.
      4. ui.navigate.to(/editor/<id>) — open the editor on the fresh draft.

    The chain is blocking (a bounded agent run), so it goes through `run.io_bound` to keep the UI
    responsive. A ValueError from any step (no linked cluster, or — the common one — no fetched
    source text the writer-agent can ground on) is surfaced as a negative notify rather than a crash,
    so the owner knows to retry or pick another story. app.fetcher / app.editor are imported lazily so
    this module's import never pulls the fetcher/LLM stacks."""
    progress = ui.notification(
        "Drafting… fetching sources and running the writer-agent", spinner=True, timeout=None
    )
    try:
        article_id = await run.io_bound(_create_and_draft, cluster_id)
    except ValueError as e:
        log.info("draft refused for cluster %s: %s", cluster_id, e)
        progress.dismiss()
        ui.notify(str(e), type="negative", multi_line=True, close_button="Dismiss")
        return
    except Exception as e:  # pragma: no cover - defensive; surfaces unexpected failures
        log.exception("draft failed for cluster %s", cluster_id)
        progress.dismiss()
        ui.notify(f"Draft failed: {type(e).__name__}: {e}", type="negative", multi_line=True)
        return
    progress.dismiss()
    ui.navigate.to(f"/editor/{article_id}")


def _create_and_draft(cluster_id: str) -> str:
    """Blocking core of the "Draft →" action (runs in a worker thread via run.io_bound).

    Opens its own session (the thread has no request scope), runs the idempotent pass-2 fetch (a
    no-op when the approved cluster's text was already pulled), creates/reopens the article, runs the
    draft, and returns the article id. The editor functions commit internally. Kept as a tiny
    module-level helper (not a lambda) so the lazy imports and the session lifetime are explicit and
    the worker thread has a clean call target. Postgres-only writes — never posts."""
    from app.editor import create_article_for_cluster, draft_article
    from app.fetcher import fetch_cluster_full_text

    with _db_session() as session:
        fetch_cluster_full_text(session, cluster_id)
        article_id = create_article_for_cluster(session, cluster_id)
        draft_article(session, article_id)
        return article_id


# --- page 2: editor (chat-drafting surface) ------------------------------------------------


def _build_editor(article_id: str) -> None:
    """Render the editor page for `article_id`, or a themed not-found if it doesn't exist.

    Layout: a header (with a live status chip, a piece-type switcher, and the Gate-2 Approve
    control), then a two-pane split — LEFT a chat (message list + input + send), RIGHT a live
    markdown preview plus a raw hand-edit textarea with a Save edits button. The chat routes
    through the existing backend (draft_article for an empty draft; the app.web.chat iterate seam
    for follow-ups); Save edits persists the textarea to articles.current_draft; the switcher
    routes a mid-stream reformat through the iterate seam; Approve moves status → pre_publish."""
    with _db_session() as session:
        view = queries.load_article(session, article_id)

    if view is None:
        _not_found(f"article {article_id!r} not found")
        return

    # Mutable per-page state shared by the closures below. `draft` is the working copy the preview
    # and textarea reflect; it starts from the persisted draft and is updated by Save edits, the
    # iterate agent, and a piece-type reformat. `piece_type` / `status` track the article's current
    # shape + lifecycle so the header controls reflect (and update) them in place. NiceGUI gives
    # each browser session its own page invocation, so this dict is safely page-local.
    state: dict = {
        "draft": view.current_draft,
        "piece_type": view.piece_type,
        "status": view.status,
    }

    _build_editor_header(article_id, state)

    with ui.splitter(value=40).classes("w-full").style(
        "height: calc(100vh - 60px)"
    ).mark("editor") as splitter:
        with splitter.before:
            _build_chat_pane(article_id, state)
        with splitter.after:
            _build_preview_pane(article_id, state)


def _build_editor_header(article_id: str, state: dict) -> None:
    """Render the editor's top bar: the home link + breadcrumb, a live status chip, the piece-type
    switcher (mid-stream reformat), the Gate-2 Approve control, and the Mark-as-published control.

    The status chip (`.mark("article-status")`) reflects `state["status"]` and updates in place
    after a successful approve OR mark-published. The piece-type `ui.select`
    (`.mark("piece-type-select")`) defaults to the article's current type and, on change, runs a
    structural reformat through the iterate seam. The Approve button (`.mark("approve-gate2")`)
    calls `approve_article` (drafting → pre_publish) and disables itself once the article is at
    pre_publish or beyond.

    The Mark-as-published button (`.mark("mark-published")`) calls `publish_article`
    (pre_publish → published + KB embedding) — it is BOOKKEEPING of the owner's external manual
    publish, never an actual post. It is meaningful only after Gate 2: enabled at `pre_publish`,
    disabled while `drafting`/`approved` (approve first) and once already `published`. The element
    is stashed on `state["_publish_btn_el"]` so the Approve handler can ENABLE it after a
    successful approve (the cross-control wiring that lights up Phase-5 controls once the canonical
    is approved)."""
    with ui.header().classes("items-center gap-4 px-4 py-2"):
        ui.link("AI Content Engine", "/").classes(
            "text-white font-semibold no-underline"
        )
        ui.label(f"{article_id}").classes("text-sm opacity-80")

        # Live status chip — reflects the lifecycle status and updates after approve.
        status_chip = (
            ui.badge(state["status"])
            .props("color=grey-8")
            .classes("text-sm")
            .mark("article-status")
        )
        state["_status_chip_el"] = status_chip

        # Push the controls to the right edge.
        ui.space()

        # Attach material (Phase 10): add owner material (pasted text / a file / a URL) to THIS
        # article. On a flagship piece this is the add-more path; on a cluster-backed piece it is
        # the FUSION path (the owner's own material joins the cluster grounding). No auto-redraft —
        # the owner iterates via chat afterward — so on submit it just refreshes the Sources panel.
        _build_attach_material_control(article_id, state)

        # Piece-type switcher — mid-stream structural reformat.
        from app.editor.article import PIECE_TYPES

        piece_select = (
            ui.select(
                list(PIECE_TYPES),
                value=state["piece_type"] if state["piece_type"] in PIECE_TYPES else None,
                label="Piece type",
            )
            .props("dense outlined dark options-dense")
            .classes("min-w-40 bg-white rounded")
            .mark("piece-type-select")
        )
        state["_piece_select_el"] = piece_select

        async def _on_piece_type_change(e) -> None:
            await _switch_piece_type(article_id, state, e.value)

        # Bind the change handler; the message list is set on state by the chat pane so the
        # reformat can post a chat note (the panes build after the header, so we look it up lazily).
        piece_select.on_value_change(_on_piece_type_change)

        # Gate-2 Approve control — drafting → pre_publish (NOT publishing). Approve is meaningful
        # only while drafting; it disables once the canonical is approved (pre_publish) or beyond
        # (published).
        approve_btn = (
            ui.button(
                "Approve (pre-publish)",
                on_click=lambda: _on_approve_click(article_id, state),
            )
            .props("color=positive unelevated")
            .mark("approve-gate2")
        )
        state["_approve_btn_el"] = approve_btn
        if state["status"] != "drafting":
            approve_btn.disable()

        # Mark-as-published control — pre_publish → published + KB embedding. This RECORDS that the
        # owner published manually elsewhere (bookkeeping that closes the lifecycle and populates
        # the knowledge base); it never posts. Meaningful only after Gate 2: enabled at pre_publish,
        # disabled while drafting/approved (approve first) and once already published.
        publish_btn = (
            ui.button(
                "Mark as published",
                on_click=lambda: _on_publish_click(article_id, state),
            )
            .props("color=primary unelevated")
            .tooltip(
                "Records that you posted this manually — flips status to published and builds "
                "the knowledge-base embedding. The system never posts anything."
            )
            .mark("mark-published")
        )
        state["_publish_btn_el"] = publish_btn
        if state["status"] != "pre_publish":
            publish_btn.disable()


# --- attach material on the editor (fusion + add-more; Phase 10) ----------------------------


def _build_attach_material_control(article_id: str, state: dict) -> None:
    """Render the editor header's "Attach material" button + its intake dialog (Phase 10).

    The button (`.mark("attach-material-button")`) opens the shared intake dialog
    (`.mark("attach-material-dialog")`) — the SAME text / file / URL inputs as the dashboard's "new
    piece", minus the piece-type select (this article already has a type). On submit it attaches
    the supplied material to the CURRENTLY-OPEN article (the add-more path on a flagship piece; the
    FUSION path on a cluster-backed one) and refreshes the Sources panel so the new material shows.
    There is NO auto-redraft — the owner iterates via chat afterward.

    The dialog also carries the Phase-10b "Find related news" control (`.mark("attach-find-related")`)
    over the dialog's text input; here it is ATTACH-CAPABLE (`fusion_attach=(article_id, state)`), so
    each result gets an "Attach as source" button that pulls that related news cluster's URL into THIS
    article as an owner grounding source (the fusion path; no article_clusters link) and refreshes the
    Sources panel."""
    dialog, form = _build_intake_dialog(
        mark_prefix="attach",
        title="Attach material",
        submit_label="Attach",
        piece_types=None,  # the article already has a piece type — no select here
        default_piece_type=None,
        on_submit=lambda: _on_attach_material_submit(article_id, state, form, dialog),
        fusion_attach=(article_id, state),  # the editor path: results are attachable as sources
    )

    ui.button("Attach material", icon="attach_file", on_click=dialog.open).props(
        "color=white outline dense"
    ).mark("attach-material-button")


async def _on_attach_material_submit(
    article_id: str, state: dict, form: dict, dialog
) -> None:
    """Handle the editor "Attach" submit: attach the owner's material to THIS article, then refresh
    the Sources panel (Phase 10). Runs the attach chain off the event loop; NO redraft.

    Validation mirrors the dashboard new-piece path: at least one of pasted text / an uploaded file
    / a URL is required (else a negative notify, dialog stays open). A URL fetch that yields nothing
    is tolerated when there is other material (warn + proceed); if the URL was the only input and it
    failed, surface the error. On success we close the dialog and rebuild the Sources panel in place
    so the new owner row appears. Never posts."""
    text, upload, url = _intake_inputs(form)
    if not (text or upload or url):
        ui.notify(
            "Add at least one of: pasted text, an uploaded file, or a source URL.",
            type="negative",
        )
        return

    submit_btn = form.get("submit_btn")
    if submit_btn is not None:
        submit_btn.disable()
    progress = ui.notification("Attaching material…", spinner=True, timeout=None)
    try:
        url_failed = await run.io_bound(
            _attach_owner_material, article_id, text, upload, url
        )
    except ValueError as e:
        progress.dismiss()
        if submit_btn is not None:
            submit_btn.enable()
        log.info("attach-material refused for article %s: %s", article_id, e)
        ui.notify(str(e), type="negative", multi_line=True, close_button="Dismiss")
        return
    except Exception as e:  # pragma: no cover - defensive; surfaces unexpected failures
        progress.dismiss()
        if submit_btn is not None:
            submit_btn.enable()
        log.exception("attach-material failed for article %s", article_id)
        ui.notify(
            f"Attach failed: {type(e).__name__}: {e}", type="negative", multi_line=True
        )
        return
    progress.dismiss()
    if submit_btn is not None:
        submit_btn.enable()
    if url_failed:
        ui.notify(
            "Could not fetch the URL — attached your other material.",
            type="warning",
            multi_line=True,
        )
    dialog.close()
    # Reset the dialog inputs so a second attach starts clean.
    _reset_intake_form(form)
    _refresh_sources(article_id, state)
    ui.notify("Material attached", type="positive")


def _attach_owner_material(
    article_id: str, text: str, upload: dict | None, url: str
) -> bool:
    """Blocking core of the editor "Attach" submit (runs in a worker thread via run.io_bound).
    Returns url_failed (True when a URL was given, yielded nothing, but other material was attached).

    Opens its own session and attaches the supplied material to `article_id` in order — pasted
    text, then the parsed uploaded file, then the fetched URL. Mirrors the flagship create chain's
    attach logic (a URL-only failure raises; a URL failure alongside other material is tolerated)
    but does NOT create or draft — the article already exists and the owner redrafts via chat.
    app.editor is imported lazily. Postgres-only writes — never posts."""
    from app.editor import (
        attach_owner_source,
        attach_owner_url,
        parse_uploaded_file,
    )

    with _db_session() as session:
        attached_any = False
        url_failed = False
        if text:
            attach_owner_source(
                session, article_id, kind="text", content=text, title="Pasted note"
            )
            attached_any = True
        if upload is not None:
            content = parse_uploaded_file(upload["name"], upload["data"])
            attach_owner_source(
                session, article_id, kind="file", title=upload["name"], content=content
            )
            attached_any = True
        if url:
            try:
                attach_owner_url(session, article_id, url)
                attached_any = True
            except ValueError:
                if not attached_any:
                    raise
                url_failed = True
                log.info(
                    "attach %s: url fetch yielded nothing, kept other material", article_id
                )
        return url_failed


def _reset_intake_form(form: dict) -> None:
    """Clear an intake form's inputs (text / url) and the captured upload after a successful attach,
    so reopening the dialog starts clean. The upload element keeps its own UI state; resetting the
    captured bytes is what matters (a stale file won't be re-attached)."""
    text_el = form.get("text_el")
    url_el = form.get("url_el")
    if text_el is not None:
        text_el.value = ""
    if url_el is not None:
        url_el.value = ""
    form["upload"] = None


def _refresh_sources(article_id: str, state: dict) -> None:
    """Rebuild the Sources panel in place from a fresh `load_article_sources` read, so newly
    attached owner material shows immediately. No-op if the panel isn't present (defensive)."""
    list_el = state.get("_sources_list_el")
    if list_el is not None:
        _render_sources_list(list_el, _load_article_sources(article_id))


def _build_chat_pane(article_id: str, state: dict) -> None:
    """LEFT pane: the chat. A scrollable message list (system intro + owner/agent bubbles), a text
    input, and a Send button. Sending routes the instruction through `_send_instruction` (which
    drives draft_article for an empty draft, or the Phase-4 chat seam for follow-ups)."""
    with ui.column().classes("w-full h-full p-2 gap-2"):
        ui.label("Chat · iterate the draft").classes(
            "text-xs uppercase tracking-wide text-gray-500"
        )
        messages = (
            ui.column()
            .classes("w-full grow overflow-auto gap-1 p-1")
            .mark("chat-messages")
        )
        # Stash the message list so header controls (the piece-type switcher) can post a chat note
        # without the chat input being involved.
        state["_messages_el"] = messages
        with messages:
            ui.chat_message(_CHAT_INTRO, name="editor").props("bg-color=grey-2")

        with ui.row().classes("w-full items-center gap-2 no-wrap"):
            text_in = (
                ui.input(placeholder="Tell the editor what to change…")
                .classes("grow")
                .props("outlined dense")
                .mark("chat-input")
            )

            async def _send() -> None:
                await _send_instruction(article_id, state, messages, text_in)

            text_in.on("keydown.enter", _send)
            ui.button(icon="send", on_click=_send).props("round dense color=primary").mark(
                "chat-send"
            )


async def _send_instruction(
    article_id: str, state: dict, messages, text_in
) -> None:
    """Send one owner chat instruction. Pure-ish UI glue around the backend seams.

    Branching:
      - If the working draft is EMPTY, the instruction (or the implicit "draft this") triggers the
        writer-agent INITIAL draft via `draft_article` (run.io_bound, off the event loop). On
        success the preview + textarea refresh from the freshly persisted draft.
      - Otherwise it routes to the Phase-4 iterate SEAM `chat_seam.handle_editor_message(...)` —
        the real edit-in-place writer-agent. We pass the CURRENT textarea value as `base_draft` so
        the owner's UNSAVED hand-edits are the base the agent edits (manual edits are sacred — hard
        rule). On return we update the working draft from the FULL revised draft the seam persisted,
        refresh the preview + textarea (edit-in-place, never regeneration), and append the agent's
        short confirmation as a chat bubble. We only CALL the seam — the agent (grounding, the
        edit_log append, the DB write) lives entirely in the backend.

    The owner's message is echoed as a chat bubble immediately; the assistant reply (or a draft
    confirmation) is appended when the backend returns. Empty/whitespace input is a no-op.

    A ValueError from the seam (e.g. an article whose draft was lost) is surfaced as a red chat
    bubble + a negative notify rather than crashing the page."""
    instruction = (text_in.value or "").strip()
    if not instruction:
        return
    text_in.value = ""
    with messages:
        ui.chat_message(instruction, name="you", sent=True).mark("msg-owner")

    if not (state["draft"] or "").strip():
        # Empty draft → run the writer-agent initial draft.
        await _generate_initial_draft(article_id, state, messages)
        return

    # Non-empty draft → route to the Phase-4 iterate seam (the real edit-in-place writer-agent).
    # Pass the LIVE textarea value as base_draft so unsaved hand-edits are respected.
    base_draft = _current_base_draft(state)
    progress = ui.notification(
        "Editing… running the writer-agent", spinner=True, timeout=None
    )
    try:
        result = await run.io_bound(
            _iterate, article_id, instruction, base_draft, None
        )
    except ValueError as e:
        progress.dismiss()
        with messages:
            ui.chat_message(f"Could not edit: {e}", name="editor").props(
                "bg-color=red-2"
            ).mark("msg-agent")
        ui.notify(str(e), type="negative", multi_line=True, close_button="Dismiss")
        return
    except Exception as e:  # pragma: no cover - defensive; surfaces unexpected failures
        progress.dismiss()
        log.exception("iterate failed for article %s", article_id)
        with messages:
            ui.chat_message(
                f"Edit failed: {type(e).__name__}: {e}", name="editor"
            ).props("bg-color=red-2").mark("msg-agent")
        ui.notify("Edit failed", type="negative", multi_line=True)
        return
    progress.dismiss()
    _apply_iterate_result(article_id, state, result)
    with messages:
        ui.chat_message(result.reply, name="editor").props("bg-color=grey-2").mark(
            "msg-agent"
        )


def _current_base_draft(state: dict) -> str | None:
    """The base the writer-agent should edit: the LIVE raw textarea value (the owner's unsaved
    hand-edits), falling back to the working draft if the textarea isn't present.

    Reading the textarea element (stashed as `state["_textarea_el"]`) — not `state["draft"]` — is
    what makes hand-edits sacred: an instruction edits whatever the owner currently sees and has
    typed into the raw pane, even if they never clicked Save. Returned as base_draft so the agent
    edits in place from there (the backend treats None as "use the persisted draft")."""
    textarea = state.get("_textarea_el")
    if textarea is not None and textarea.value is not None:
        return textarea.value
    return state.get("draft")


def _iterate(
    article_id: str, instruction: str, base_draft: str | None, new_piece_type: str | None
):
    """Blocking core of an iterate / piece-type-switch call (runs in a worker thread via
    run.io_bound). Thin wrapper over the chat seam so the lazy nature and the call target are
    explicit. The seam opens its OWN DB session, runs the writer-agent iterate (model call + DB
    write, including the edit_log append), and returns an IterateResult — we never touch the DB or
    the agent here."""
    return chat_seam.handle_editor_message(
        article_id,
        instruction,
        base_draft=base_draft,
        new_piece_type=new_piece_type,
    )


def _apply_iterate_result(article_id: str, state: dict, result) -> None:
    """Apply an IterateResult to the page: update the working draft + piece_type from the result and
    refresh the preview + textarea so both panes show the edit-in-place outcome.

    `result.draft` is the FULL revised current_draft the seam already persisted, so we mirror it
    verbatim (no regeneration on our side). `result.piece_type` may have changed (on a switch); we
    keep `state["piece_type"]` and the header select in sync so the UI never drifts from the DB. The
    iterate appended a new edit_log entry, so we rebuild the version-history panel too."""
    state["draft"] = result.draft
    state["piece_type"] = result.piece_type
    _refresh_draft_views(state)
    _refresh_history(article_id, state)
    select = state.get("_piece_select_el")
    if select is not None and select.value != result.piece_type:
        # Keep the switcher in sync without re-triggering its change handler loop — assigning the
        # same value the backend reports is idempotent (NiceGUI only fires on an actual change).
        select.value = result.piece_type


async def _generate_initial_draft(article_id: str, state: dict, messages) -> None:
    """Run the writer-agent INITIAL draft for an empty-draft article, then refresh the panes.

    Calls `draft_article` off the event loop (run.io_bound). A grounding refusal (the cluster has
    no fetched source text yet) or any other ValueError is shown as a system chat note + a notify
    rather than a crash. On success the persisted draft is loaded back into `state["draft"]` and
    the preview + textarea are refreshed. app.editor is imported lazily."""
    progress = ui.notification(
        "Drafting… running the writer-agent", spinner=True, timeout=None
    )
    try:
        draft = await run.io_bound(_draft_existing_article, article_id)
    except ValueError as e:
        progress.dismiss()
        with messages:
            ui.chat_message(f"Could not draft: {e}", name="editor").props("bg-color=red-2")
        ui.notify(str(e), type="negative", multi_line=True, close_button="Dismiss")
        return
    progress.dismiss()
    state["draft"] = draft
    _refresh_draft_views(state)
    _refresh_history(article_id, state)
    with messages:
        ui.chat_message(
            "Initial draft generated — review it on the right. "
            "Tell me what to change to iterate.",
            name="editor",
        ).props("bg-color=grey-2")


def _draft_existing_article(article_id: str) -> str:
    """Blocking core of the initial-draft path (runs in a worker thread). Opens its own session,
    runs draft_article (which persists current_draft and commits), returns the draft text."""
    from app.editor import draft_article

    with _db_session() as session:
        return draft_article(session, article_id)


# --- piece-type switch (mid-stream reformat) -----------------------------------------------


async def _switch_piece_type(article_id: str, state: dict, chosen: str | None) -> None:
    """Handle a piece-type select change: run a structural reformat through the iterate seam.

    Switching piece type is a STRUCTURAL REFORMAT, not a point edit (docs §2.3) — but it goes
    through the SAME `handle_editor_message` seam, with `new_piece_type=…`, so the agent reformats
    the working draft in place (the owner's content survives; only the shape changes). We pass the
    LIVE textarea value as `base_draft` so any unsaved hand-edits are respected during the reformat.

    No-op if the choice is empty or unchanged (NiceGUI may emit a value-change on programmatic
    re-sync — we guard against re-entering on the same type). On success the preview + textarea
    refresh from the revised draft and a chat note records the switch; a ValueError or unexpected
    failure surfaces as a notify (and the select snaps back to the article's actual type)."""
    if not chosen or chosen == state.get("piece_type"):
        return
    previous = state.get("piece_type")
    messages = state.get("_messages_el")
    base_draft = _current_base_draft(state)
    instruction = f"Reformat this draft as a {chosen} piece."
    progress = ui.notification(
        f"Reformatting as {chosen}… running the writer-agent",
        spinner=True,
        timeout=None,
    )
    try:
        result = await run.io_bound(
            _iterate, article_id, instruction, base_draft, chosen
        )
    except ValueError as e:
        progress.dismiss()
        _resync_piece_select(state, previous)
        ui.notify(str(e), type="negative", multi_line=True, close_button="Dismiss")
        return
    except Exception as e:  # pragma: no cover - defensive; surfaces unexpected failures
        progress.dismiss()
        log.exception("piece-type switch failed for article %s", article_id)
        _resync_piece_select(state, previous)
        ui.notify(
            f"Reformat failed: {type(e).__name__}: {e}",
            type="negative",
            multi_line=True,
        )
        return
    progress.dismiss()
    _apply_iterate_result(article_id, state, result)
    ui.notify(f"Reformatted as {result.piece_type}", type="positive")
    if messages is not None:
        with messages:
            ui.chat_message(
                f"Piece type switched to {result.piece_type} — the draft was reformatted "
                "in place. Review it on the right.",
                name="editor",
            ).props("bg-color=grey-2").mark("msg-agent")


def _resync_piece_select(state: dict, value: str | None) -> None:
    """Snap the piece-type select back to `value` (the article's actual type) after a failed switch,
    so the dropdown never shows a type the backend didn't apply. Idempotent (NiceGUI fires only on
    a real change), and the no-op guard in `_switch_piece_type` keeps this from looping."""
    select = state.get("_piece_select_el")
    if select is not None and select.value != value:
        select.value = value


# --- Gate 2: approve (drafting → pre_publish; NOT publishing) -------------------------------


async def _on_approve_click(article_id: str, state: dict) -> None:
    """Handle the Gate-2 Approve click: move the article drafting → pre_publish, off the event loop.

    This is the owner's approval of the canonical draft (Gate 2) — NOT publishing. On success we
    update the status chip + working state, disable the Approve button (idempotent re-approve is
    harmless, but a disabled control reads clearly), and — the Phase-5 cross-control wiring — light
    up the controls that only make sense AFTER Gate 2: the Mark-as-published button and the
    per-platform variant generate buttons. A ValueError (e.g. the article is already published)
    surfaces as a negative notify. Nothing here posts anywhere (hard rule)."""
    progress = ui.notification("Approving…", spinner=True, timeout=None)
    try:
        new_status = await run.io_bound(_approve, article_id)
    except ValueError as e:
        progress.dismiss()
        ui.notify(str(e), type="negative", multi_line=True, close_button="Dismiss")
        return
    except Exception as e:  # pragma: no cover - defensive; surfaces unexpected failures
        progress.dismiss()
        log.exception("approve failed for article %s", article_id)
        ui.notify(f"Approve failed: {type(e).__name__}: {e}", type="negative", multi_line=True)
        return
    progress.dismiss()
    state["status"] = new_status
    chip = state.get("_status_chip_el")
    if chip is not None:
        chip.set_text(new_status)
    btn = state.get("_approve_btn_el")
    if btn is not None and new_status != "drafting":
        btn.disable()
    # Cross-control wiring: pre_publish is the gate for both mark-published and variant generation.
    if new_status == "pre_publish":
        publish_btn = state.get("_publish_btn_el")
        if publish_btn is not None:
            publish_btn.enable()
        _set_variant_controls_enabled(state, True)
    ui.notify(f"Approved — status is now {new_status}", type="positive")


def _approve(article_id: str) -> str:
    """Blocking core of Gate-2 approve (runs in a worker thread). Opens its own short-lived session
    (mirrors `_persist_draft`) and calls `approve_article`, which moves drafting → pre_publish and
    commits, returning the new status. Idempotent for an already-pre_publish article; raises
    ValueError for a published one. app.editor is imported lazily. Never publishes."""
    from app.editor import approve_article

    with _db_session() as session:
        return approve_article(session, article_id)


# --- mark as published (pre_publish → published; BOOKKEEPING, NOT publishing) ----------------


async def _on_publish_click(article_id: str, state: dict) -> None:
    """Handle the Mark-as-published click: move the article pre_publish → published, off the event
    loop, and compute the KB embedding.

    This is NOT publishing. The owner has already posted the article MANUALLY (LinkedIn / Medium /
    Reddit) — this control RECORDS that external act: it flips the lifecycle status to `published`
    and builds the article embedding so the published piece joins the knowledge base for future
    voice/continuity retrieval. The system never posts anything (hard rule). On success we update
    the status chip + working state and disable this button (already published) — Approve stays
    disabled (no longer pre_publish). A ValueError (the article isn't at pre_publish — Gate 2 must
    happen first — or the draft is empty) surfaces as a negative notify."""
    progress = ui.notification("Recording the manual post…", spinner=True, timeout=None)
    try:
        new_status = await run.io_bound(_publish, article_id)
    except ValueError as e:
        progress.dismiss()
        ui.notify(str(e), type="negative", multi_line=True, close_button="Dismiss")
        return
    except Exception as e:  # pragma: no cover - defensive; surfaces unexpected failures
        progress.dismiss()
        log.exception("mark-published failed for article %s", article_id)
        ui.notify(
            f"Mark as published failed: {type(e).__name__}: {e}",
            type="negative",
            multi_line=True,
        )
        return
    progress.dismiss()
    state["status"] = new_status
    chip = state.get("_status_chip_el")
    if chip is not None:
        chip.set_text(new_status)
    publish_btn = state.get("_publish_btn_el")
    if publish_btn is not None and new_status == "published":
        publish_btn.disable()
    ui.notify(f"Marked as published — status is now {new_status}", type="positive")


def _publish(article_id: str) -> str:
    """Blocking core of mark-as-published (runs in a worker thread). Opens its own short-lived
    session and calls `publish_article`, which moves pre_publish → published, computes + stores the
    KB embedding, and commits, returning the new status ("published"). Raises ValueError if the
    article isn't at pre_publish (Gate 2 first) or the draft is empty. app.editor is imported
    lazily. This is bookkeeping of an external manual publish — it never posts anywhere."""
    from app.editor import publish_article

    with _db_session() as session:
        return publish_article(session, article_id)


def _build_preview_pane(article_id: str, state: dict) -> None:
    """RIGHT pane: the live preview + raw hand-edit + the variants section. Top is the rich preview
    container of the current draft (markdown with syntax-highlighted fenced code, and ```mermaid
    blocks rendered as diagrams via `_render_draft_preview`); below is a `ui.textarea` holding the raw
    markdown with a Save edits button that persists the textarea to articles.current_draft (the
    hand-edit path that respects manual edits); below THAT is the per-platform variants section
    (copy-out text the owner posts manually)."""
    with ui.column().classes("w-full h-full p-2 gap-2 overflow-auto"):
        ui.label("Live preview · current draft").classes(
            "text-xs uppercase tracking-wide text-gray-500"
        )
        # The preview is a CONTAINER (not a single ui.markdown) so the rich renderer can split the
        # draft into markdown segments (highlighted fenced code) + ```mermaid diagram segments and
        # rebuild them in place on every refresh.
        preview = ui.column().classes("w-full gap-2").mark("preview")
        _render_draft_preview(preview, _preview_text(state["draft"]))

        ui.label("Raw draft · hand-edit").classes(
            "text-xs uppercase tracking-wide text-gray-500 mt-2"
        )
        editor_area = (
            ui.textarea(value=state["draft"] or "")
            .props("outlined autogrow")
            .classes("w-full font-mono")
            .mark("draft-textarea")
        )

        # Stash the elements on state so the draft-refresh helper (used after an agent draft) can
        # update them without threading them through every call.
        state["_preview_el"] = preview
        state["_textarea_el"] = editor_area

        async def _save() -> None:
            await _save_edits(article_id, state, editor_area)

        ui.button("Save edits", on_click=_save).props(
            "color=primary unelevated"
        ).mark("save-edits")

        # Phase 5: the per-platform variants section, below Save edits in the same scroll column.
        _build_variants_section(article_id, state)

        # The SOURCES panel — the original articles behind the draft, opened in a new tab for the
        # owner to re-read (read-only links; the system never posts).
        _build_sources_panel(article_id, state)

        # The VERSION HISTORY panel — the edit_log as a restorable, diffable timeline.
        _build_history_panel(article_id, state)


# --- variants (per-platform copy-out text; NEVER posts) ------------------------------------


# Per-platform display labels for the variant cards. The variants section ITERATES
# `app.variants.PLATFORMS`, so a new platform (e.g. "x") gets a card automatically; this map gives
# each one an owner-friendly label (capitalised platform name otherwise). "x" reads as "X / Twitter"
# so the card names the platform unambiguously.
_PLATFORM_LABELS = {
    "medium": "Medium",
    "reddit": "Reddit",
    "linkedin": "LinkedIn",
    "x": "X / Twitter",
}

# Per-platform Quasar accent colour for the variant card's platform chip (a small coloured pill that
# names the target platform). Theme-aware Quasar colour names (no raw hex), consistent with the rest
# of the file. An unmapped platform falls back to a neutral grey.
_PLATFORM_CHIP_COLORS = {
    "medium": "green-7",
    "reddit": "deep-orange-6",
    "linkedin": "blue-8",
    "x": "blue-grey-9",
}


def _platform_label(platform: str) -> str:
    """The owner-facing label for a variant platform ("X / Twitter" for "x"); falls back to the
    capitalised platform name for any platform not in `_PLATFORM_LABELS`."""
    return _PLATFORM_LABELS.get(platform, platform.capitalize())


def _platform_chip_color(platform: str) -> str:
    """The Quasar chip colour for a variant platform (neutral grey for any unmapped platform)."""
    return _PLATFORM_CHIP_COLORS.get(platform, "grey-6")


def _build_variants_section(article_id: str, state: dict) -> None:
    """Render the variants section: for each platform a Generate button, a Save button, and an
    EDITABLE output area.

    A variant is the canonical reformatted/condensed for ONE platform (Medium / Reddit / LinkedIn /
    X / Twitter), produced on demand by a single backend model call. It is COPY-OUT TEXT ONLY — the
    owner selects it and posts MANUALLY; there is deliberately no posting button or share integration
    (hard rule:
    the system never publishes). The output field is EDITABLE so the owner can hand-tune the wording
    inline, and a per-platform Save button persists that tweak back (a plain DB write via
    `save_variant_edit` — NO model call, never posts). Variants are derived AFTER Gate 2, so the
    Generate + Save buttons are enabled only when the article is at `pre_publish`/`published`; while
    `drafting` they are disabled with a hint to approve first, and the Approve handler enables them in
    place after a successful Gate-2 approve.

    On page load, any existing latest variant per platform is prefilled into its output area (read
    back via `list_latest_variants`); otherwise the area starts empty. The platform list and the
    generate/list/save helpers are imported lazily inside the worker helpers so importing this module
    never pulls the LLM/variants stack.

    Each platform's output textarea is stashed on `state["_variant_out_els"][platform]` and both its
    Generate and Save buttons on `state["_variant_gen_btns"]` (the shared enable/disable group) so the
    generate handler can push fresh text, the save handler can read the field, and the Approve handler
    can flip them all enabled together."""
    from app.variants import PLATFORMS

    variants_enabled = state["status"] in ("pre_publish", "published")
    existing = _load_latest_variants(article_id)

    state.setdefault("_variant_out_els", {})
    state.setdefault("_variant_gen_btns", [])

    with ui.column().classes("w-full gap-2 mt-4").mark("variants-section"):
        ui.label("Platform variants · copy-out").classes(
            "text-xs uppercase tracking-wide text-gray-500"
        )
        ui.label(
            "Generate platform-ready text, then COPY it and post manually — the system never "
            "posts anything. Available after Gate-2 approval."
        ).classes("text-xs text-gray-500")
        if not variants_enabled:
            state["_variant_gate_hint_el"] = (
                ui.label("Approve the canonical (Gate 2) first.")
                .classes("text-xs italic text-gray-500")
                .mark("variants-gate-hint")
            )

        # Iterate the PLATFORMS tuple (not a hardcoded list) so every supported platform gets a card
        # automatically — including "x" (X / Twitter), with the standard variant-card-x / gen-variant-x
        # / variant-out-x / save-variant-x marks and the same Gate-2 gating as the others.
        for platform in PLATFORMS:
            _build_variant_block(
                article_id, state, platform, existing.get(platform, ""), variants_enabled
            )


def _build_variant_block(
    article_id: str, state: dict, platform: str, prefill: str, enabled: bool
) -> None:
    """One platform's variant block: a coloured platform chip, a Generate button, a Save button, and
    an EDITABLE output area. Called once per platform in `app.variants.PLATFORMS` (so "x" gets the
    same card as the others); the owner-facing label comes from `_platform_label` ("X / Twitter").

    The Generate button (`.mark(f"gen-variant-{platform}")`) runs `generate_variant` off the event
    loop and pushes the formatted text into the output area. The output (`.mark(f"variant-out-
    {platform}")`) is an EDITABLE textarea (copy-friendly: the owner selects + copies it; and
    hand-tunable: the owner can tweak the wording inline) prefilled with the latest stored variant if
    one exists. The Save button (`.mark(f"save-variant-{platform}")`) persists the owner's hand-tuned
    text back via `save_variant_edit` (a plain DB write — NO model call, never posts) and echoes the
    saved text into the field. All three controls are gated together: Generate + Save are enabled only
    at pre_publish/published (variants are derived after Gate 2), and the Approve handler lights them
    up in place after a successful approve. Both buttons join `state["_variant_gen_btns"]` (the shared
    enable/disable group) and the output is stashed on `state["_variant_out_els"]`."""
    label = _platform_label(platform)
    with ui.card().classes("w-full gap-2 p-3").mark(f"variant-card-{platform}"):
        with ui.row().classes("w-full items-center gap-2"):
            # A small per-platform coloured chip names the target platform at a glance ("X / Twitter"
            # for "x"); the colour comes from `_platform_chip_color`.
            ui.badge(label).props(f"color={_platform_chip_color(platform)}").classes(
                "text-xs whitespace-nowrap"
            )
            gen_btn = (
                ui.button(
                    f"Generate {label}",
                    on_click=lambda p=platform: _on_generate_variant_click(
                        article_id, state, p
                    ),
                )
                .props("color=primary unelevated dense")
                .mark(f"gen-variant-{platform}")
            )
            save_btn = (
                ui.button(
                    f"Save {label}",
                    on_click=lambda p=platform: _on_save_variant_click(
                        article_id, state, p
                    ),
                )
                .props("color=primary outline dense")
                .mark(f"save-variant-{platform}")
            )
            if not enabled:
                gen_btn.disable()
                save_btn.disable()
            # Both buttons join the shared enable/disable group (lit up together after Gate 2).
            state["_variant_gen_btns"].append(gen_btn)
            state["_variant_gen_btns"].append(save_btn)

        out = (
            ui.textarea(value=prefill)
            .props('outlined autogrow input-class=font-mono')
            .classes("w-full")
            .mark(f"variant-out-{platform}")
        )
        if not prefill:
            out.props(f'placeholder="No {label} variant yet — click Generate {label}."')
        state["_variant_out_els"][platform] = out


def _set_variant_controls_enabled(state: dict, enabled: bool) -> None:
    """Enable/disable all per-platform variant controls (Generate AND Save buttons) in one shot —
    they share `state["_variant_gen_btns"]` (defensive on missing elements). Called by the Approve
    handler to light up variant generation + hand-tune-save once the article reaches pre_publish
    (variants are derived after Gate 2)."""
    for btn in state.get("_variant_gen_btns", []):
        if enabled:
            btn.enable()
        else:
            btn.disable()
    hint = state.get("_variant_gate_hint_el")
    if hint is not None and enabled:
        hint.set_visibility(False)


async def _on_generate_variant_click(article_id: str, state: dict, platform: str) -> None:
    """Handle a "Generate {Platform}" click: run the single backend model call off the event loop and
    push the formatted text into that platform's read-only output area for the owner to copy.

    `generate_variant` requires the article be at pre_publish/published with a non-empty draft (a
    ValueError otherwise) — the gating disables the button before then, but we still surface a
    ValueError as a negative notify rather than crashing (mirrors the Draft action). The system
    never posts — this only produces text for the owner to copy and post manually."""
    label = platform.capitalize()
    progress = ui.notification(
        f"Generating {label} variant…", spinner=True, timeout=None
    )
    try:
        result = await run.io_bound(_generate_variant, article_id, platform)
    except ValueError as e:
        progress.dismiss()
        ui.notify(str(e), type="negative", multi_line=True, close_button="Dismiss")
        return
    except Exception as e:  # pragma: no cover - defensive; surfaces unexpected failures
        progress.dismiss()
        log.exception("variant generation failed for article %s / %s", article_id, platform)
        ui.notify(
            f"Generate {label} failed: {type(e).__name__}: {e}",
            type="negative",
            multi_line=True,
        )
        return
    progress.dismiss()
    out = state.get("_variant_out_els", {}).get(platform)
    if out is not None:
        out.value = result.formatted_text
    ui.notify(f"{label} variant ready — select and copy it to post manually", type="positive")


def _generate_variant(article_id: str, platform: str):
    """Blocking core of a variant generation (runs in a worker thread via run.io_bound). Opens its
    own short-lived session and calls `generate_variant`, which validates the platform + article
    status, does ONE model call, stores the variant, and returns a VariantResult. app.variants is
    imported lazily so this module's import never pulls the LLM stack. Never publishes."""
    from app.variants import generate_variant

    with _db_session() as session:
        return generate_variant(session, article_id, platform)


async def _on_save_variant_click(article_id: str, state: dict, platform: str) -> None:
    """Handle a "Save {Platform}" click: persist the owner's hand-tuned variant text back to the DB,
    off the event loop, then echo the saved text into the field.

    This is the MANUAL hand-tune persistence path — a plain DB write, NOT a model call. The owner has
    edited the (now editable) variant field inline; this saves exactly that text via
    `save_variant_edit`, then sets the field to `result.formatted_text` (the capped/echoed saved
    text) so the field reflects what landed in the store. `save_variant_edit` requires the article to
    exist and the text to be non-empty (a ValueError otherwise) — the gating disables the button
    before Gate 2, but we still surface a ValueError as a negative notify rather than crashing
    (mirrors the generate handler). The system never posts — this only persists copy-out text the
    owner posts manually."""
    label = platform.capitalize()
    out = state.get("_variant_out_els", {}).get(platform)
    text = (out.value if out is not None else "") or ""
    progress = ui.notification(f"Saving {label} variant…", spinner=True, timeout=None)
    try:
        result = await run.io_bound(_save_variant, article_id, platform, text)
    except ValueError as e:
        progress.dismiss()
        ui.notify(str(e), type="negative", multi_line=True, close_button="Dismiss")
        return
    except Exception as e:  # pragma: no cover - defensive; surfaces unexpected failures
        progress.dismiss()
        log.exception("variant save failed for article %s / %s", article_id, platform)
        ui.notify(
            f"Save {label} failed: {type(e).__name__}: {e}",
            type="negative",
            multi_line=True,
        )
        return
    progress.dismiss()
    if out is not None:
        out.value = result.formatted_text
    ui.notify("Saved", type="positive")


def _save_variant(article_id: str, platform: str, text: str):
    """Blocking core of a variant hand-tune save (runs in a worker thread via run.io_bound). Opens
    its own short-lived session and calls `save_variant_edit`, which validates the platform, requires
    the article + non-empty text, caps the text, no-ops if unchanged (else appends a variants row),
    and returns a VariantResult. NO model call, never publishes. app.variants is imported lazily so
    this module's import never pulls the LLM stack."""
    from app.variants import save_variant_edit

    with _db_session() as session:
        return save_variant_edit(session, article_id, platform, text)


def _load_latest_variants(article_id: str) -> dict[str, str]:
    """The latest stored variant text per platform, for prefilling the output areas on page load:
    {platform: formatted_text}. Opens its own short-lived session and calls `list_latest_variants`
    (SELECT-only), mapping each VariantResult to its formatted_text. app.variants is imported lazily.
    Returns an empty dict when there are no variants yet."""
    from app.variants import list_latest_variants

    with _db_session() as session:
        latest = list_latest_variants(session, article_id)
    return {platform: result.formatted_text for platform, result in latest.items()}


# --- sources panel (original articles; read-only, opens in a new tab; NEVER posts) ---------


def _build_sources_panel(article_id: str, state: dict) -> None:
    """Render the SOURCES panel: the original articles behind this draft, each a clickable link that
    opens in a NEW TAB so the owner can re-read the source.

    These are derived from the clusters linked to the article (article_clusters) and the items in
    them, deduped per URL by `queries.load_article_sources`. Each row is a `ui.link(title, url)`
    opened in a new tab plus a small muted chip listing the source types that observed the URL
    (e.g. "rss", "x_user"). When there are no linked sources the panel shows a muted placeholder.

    Read-only by design: these links just open the original article in the browser — the system
    never posts anything (hard rule). Loaded when the editor page builds. The list container is
    stashed on `state["_sources_list_el"]` so a refresh can rebuild it in place (currently only the
    initial build populates it, but keeping the seam mirrors the history panel)."""
    sources = _load_article_sources(article_id)

    with ui.column().classes("w-full gap-2 mt-4").mark("sources-panel"):
        ui.label("Sources · original articles").classes(
            "text-xs uppercase tracking-wide text-gray-500"
        )
        list_el = ui.column().classes("w-full gap-1")
        state["_sources_list_el"] = list_el
        _render_sources_list(list_el, sources)


def _render_sources_list(list_el, sources: list) -> None:
    """Populate the sources list container with one row per source (or a placeholder when empty).

    Clears the container first so it can be rebuilt in place. A URL-bearing source (a cluster item)
    renders as a clickable link opened in a NEW TAB; an OWNER row with no URL (pasted text / an
    uploaded file — Phase 10) renders as a plain title label (no broken empty-href link). Each row
    also shows its source-type chips: pipeline types (hn/rss/x_user/…) in a neutral grey, and an
    OWNER chip in a distinct deep-purple so the owner's own material stands out from third-party
    sources."""
    list_el.clear()
    with list_el:
        if not sources:
            ui.label("No source links for this article.").classes(
                "text-xs italic text-gray-500"
            ).mark("sources-empty")
            return
        for src in sources:
            with ui.row().classes("w-full items-center gap-2 no-wrap"):
                if src.url:
                    ui.link(src.title or src.url, src.url, new_tab=True).classes(
                        "text-primary truncate"
                    )
                else:
                    # An owner row with no URL (pasted text / uploaded file): title only, never a
                    # broken empty-href link.
                    ui.label(src.title or "(owner material)").classes(
                        "truncate"
                    )
                for source_type in src.source_types or []:
                    ui.badge(source_type).props(
                        f"color={_source_chip_color(source_type)}"
                    ).classes("text-xs whitespace-nowrap").mark(
                        f"source-chip-{source_type}"
                    )


def _load_article_sources(article_id: str) -> list:
    """The deduped original-article sources behind this draft, for the SOURCES panel. Opens its own
    short-lived session and calls `queries.load_article_sources` (SELECT-only); may return [].

    The SOURCES panel is a secondary, read-only convenience — a read failure here must NOT take down
    the whole editor page (the chat + preview + hand-edit are what the owner needs). So we degrade to
    an empty list (rendered as the muted placeholder) and log, rather than letting the page crash."""
    try:
        with _db_session() as session:
            return queries.load_article_sources(session, article_id)
    except Exception:  # pragma: no cover - defensive; the panel degrades to the empty placeholder
        log.exception("loading article sources failed for %s", article_id)
        return []


# --- version history panel (the edit_log as a diffable, restorable timeline) ----------------


def _build_history_panel(article_id: str, state: dict) -> None:
    """Render the VERSION HISTORY panel: the article's draft versions (the edit_log timeline) as a
    list, each with a "View diff" and (unless it equals the current draft / the article is published)
    a "Restore" button.

    Versions come from `queries.load_article_versions` (oldest-first; always at least one — a
    synthetic genesis when there is no edit_log yet). For each version we show its seq, the
    instruction that produced it, the timestamp, and a "genesis" tag on the genesis entry. The
    container is stashed on `state["_history_list_el"]` so the panel can be rebuilt in place after a
    chat iterate, a piece-type switch, a save, or a restore (so it always reflects the current
    edit_log). The whole panel is read/restore/inspect only — it never posts (hard rule)."""
    with ui.column().classes("w-full gap-2 mt-4").mark("history-panel"):
        ui.label("Version history").classes(
            "text-xs uppercase tracking-wide text-gray-500"
        )
        list_el = ui.column().classes("w-full gap-1")
        state["_history_list_el"] = list_el
        _render_history_list(article_id, state, list_el)


def _render_history_list(article_id: str, state: dict, list_el) -> None:
    """Populate the history list container with one card per version (oldest-first).

    Clears the container then rebuilds it from a fresh `load_article_versions` read, so the panel
    always reflects the latest edit_log after an iterate/save/restore. The current draft is matched
    against each version's text to disable Restore for the version that already equals it; Restore is
    also disabled for a published article (its canonical is frozen — hard rule)."""
    versions = _load_article_versions(article_id)
    only_one = len(versions) <= 1
    published = state.get("status") == "published"
    current_draft = state.get("draft") or ""

    list_el.clear()
    with list_el:
        if not versions:  # defensive — the contract guarantees >=1
            ui.label("No version history yet.").classes(
                "text-xs italic text-gray-500"
            ).mark("history-empty")
            return
        for version in versions:
            _render_history_row(
                article_id,
                state,
                version,
                versions,
                only_one=only_one,
                published=published,
                is_current=(version.draft or "") == current_draft,
            )


def _render_history_row(
    article_id: str,
    state: dict,
    version,
    versions: list,
    *,
    only_one: bool,
    published: bool,
    is_current: bool,
) -> None:
    """One version card: seq + instruction + timestamp (+ a genesis tag), a View-diff button, and a
    Restore button.

    View-diff opens a dialog with a unified diff (computed in Python) between the PREVIOUS version's
    draft and this version's draft (for the genesis, its full text is the baseline). Restore calls
    `restore_article_version` off the event loop and refreshes the preview + textarea + history; it
    is disabled when this version already equals the current draft, when it is the only version
    (nothing to restore to), and when the article is published (the canonical is frozen)."""
    when = _format_ts(getattr(version, "created_at", None))
    with ui.card().classes("w-full gap-1 p-2").mark(f"history-row-{version.seq}"):
        with ui.row().classes("w-full items-center gap-2 no-wrap"):
            ui.label(f"#{version.seq}").classes("text-xs font-mono text-gray-500")
            if getattr(version, "is_genesis", False):
                ui.badge("genesis").props("color=grey-6").classes("text-xs")
            ui.label(version.instruction or "(edit)").classes(
                "grow text-sm truncate"
            )
            if when:
                ui.label(when).classes("text-xs text-gray-400 whitespace-nowrap")
        with ui.row().classes("gap-2 items-center"):
            ui.button(
                "View diff",
                on_click=lambda v=version: _open_diff_dialog(v, versions),
            ).props("flat dense color=primary").mark(f"diff-{version.seq}")
            if not only_one:
                restore_btn = (
                    ui.button(
                        "Restore",
                        on_click=lambda v=version: _on_restore_click(
                            article_id, state, v
                        ),
                    )
                    .props("flat dense color=secondary")
                    .mark(f"restore-{version.seq}")
                )
                if published or is_current:
                    restore_btn.disable()


def _open_diff_dialog(version, versions: list) -> None:
    """Open a dialog showing a unified diff between the PREVIOUS version's draft and THIS version's.

    The diff is computed in Python with `difflib.unified_diff` over the two drafts' lines, then
    rendered as a monospaced block with per-line colour (added lines green, removed lines red,
    hunk/header lines muted). For the genesis (no previous version) there is nothing to diff against,
    so we show its full text as the baseline instead."""
    previous = _previous_version(version, versions)
    if previous is None:
        body_html = _baseline_html(version.draft or "")
    else:
        body_html = _unified_diff_html(
            previous.draft or "",
            version.draft or "",
            from_label=f"#{previous.seq}",
            to_label=f"#{version.seq}",
        )
    with ui.dialog() as dialog, ui.card().classes("w-full max-w-3xl").mark(
        f"diff-dialog-{version.seq}"
    ):
        ui.label(f"Diff · version #{version.seq}").classes("text-sm font-semibold")
        ui.html(body_html).classes("w-full overflow-auto")
        ui.button("Close", on_click=dialog.close).props("flat dense color=primary")
    dialog.open()


def _previous_version(version, versions: list):
    """The version immediately before `version` in the oldest-first list, or None for the genesis /
    first entry (matched by seq, which is unique and ordered)."""
    prev = None
    for v in versions:
        if v.seq == version.seq:
            return prev
        prev = v
    return prev


def _unified_diff_html(
    before: str, after: str, *, from_label: str, to_label: str
) -> str:
    """A unified diff of `before` → `after` as colour-coded HTML (added green, removed red).

    Computed with `difflib.unified_diff` over splitlines (so an empty draft diffs cleanly). Each
    line is HTML-escaped and wrapped in a coloured <span>; the whole thing is one monospaced <pre>.
    When the two drafts are identical the diff is empty, so we say so explicitly."""
    diff = list(
        difflib.unified_diff(
            before.splitlines(),
            after.splitlines(),
            fromfile=from_label,
            tofile=to_label,
            lineterm="",
        )
    )
    if not diff:
        return (
            '<pre style="white-space:pre-wrap;font-family:monospace;margin:0">'
            "<span style=\"color:#888\">No changes between these versions.</span></pre>"
        )
    lines = []
    for line in diff:
        escaped = _html.escape(line)
        if line.startswith("+++") or line.startswith("---") or line.startswith("@@"):
            color = "#888"
        elif line.startswith("+"):
            color = "#15803d"  # green-700
        elif line.startswith("-"):
            color = "#b91c1c"  # red-700
        else:
            color = "inherit"
        lines.append(f'<span style="color:{color}">{escaped}</span>')
    return (
        '<pre style="white-space:pre-wrap;font-family:monospace;margin:0">'
        + "\n".join(lines)
        + "</pre>"
    )


def _baseline_html(text: str) -> str:
    """The genesis baseline rendered as a plain monospaced block (no previous version to diff)."""
    escaped = _html.escape(text) if text else "(empty)"
    return (
        '<pre style="white-space:pre-wrap;font-family:monospace;margin:0">'
        + escaped
        + "</pre>"
    )


async def _on_restore_click(article_id: str, state: dict, version) -> None:
    """Handle a Restore click: set the article's current_draft back to `version`'s draft (logged as
    a new edit_log entry by the backend), off the event loop, then refresh the preview + textarea +
    history panel.

    Restore goes through `restore_article_version` (which appends a restore entry to edit_log so the
    timeline records it, then commits) — it is a draft mutation, never a post. On success we mirror
    the restored draft into the working state and refresh both panes plus rebuild the history panel
    (the restore is itself a new version). A ValueError (e.g. the article is published — its canonical
    is frozen) surfaces as a negative notify rather than a crash."""
    progress = ui.notification(
        f"Restoring version #{version.seq}…", spinner=True, timeout=None
    )
    try:
        draft = await run.io_bound(_restore_version, article_id, version.edit_log_id)
    except ValueError as e:
        progress.dismiss()
        ui.notify(str(e), type="negative", multi_line=True, close_button="Dismiss")
        return
    except Exception as e:  # pragma: no cover - defensive; surfaces unexpected failures
        progress.dismiss()
        log.exception("restore failed for article %s", article_id)
        ui.notify(
            f"Restore failed: {type(e).__name__}: {e}", type="negative", multi_line=True
        )
        return
    progress.dismiss()
    state["draft"] = draft
    _refresh_draft_views(state)
    _refresh_history(article_id, state)
    ui.notify(f"Restored version #{version.seq}", type="positive")


def _restore_version(article_id: str, edit_log_id: int | None) -> str:
    """Blocking core of Restore (runs in a worker thread via run.io_bound). Opens its own short-lived
    session and calls `restore_article_version`, which sets current_draft to that version, logs the
    restore to edit_log, commits, and returns the restored draft text. Raises ValueError for a
    published article. app.editor is imported lazily so this module's import never pulls the stack.
    This is a draft restore — it never posts anything."""
    from app.editor import restore_article_version

    with _db_session() as session:
        return restore_article_version(session, article_id, edit_log_id)


def _load_article_versions(article_id: str) -> list:
    """The article's draft versions (the edit_log timeline) oldest-first, for the history panel.
    Opens its own short-lived session and calls `queries.load_article_versions` (SELECT-only); the
    contract guarantees at least one entry (a synthetic genesis fallback).

    The history panel is a secondary, read-only convenience — a read failure here must NOT take down
    the whole editor page. So we degrade to an empty list (rendered as the muted placeholder) and
    log, rather than letting the page crash."""
    try:
        with _db_session() as session:
            return queries.load_article_versions(session, article_id)
    except Exception:  # pragma: no cover - defensive; the panel degrades to the empty placeholder
        log.exception("loading article versions failed for %s", article_id)
        return []


def _refresh_history(article_id: str, state: dict) -> None:
    """Rebuild the version-history list in place from a fresh edit_log read, so the panel stays
    current after a chat iterate, a piece-type switch, a save, or a restore. No-op if the panel
    isn't present (defensive — e.g. a not-found page never builds it)."""
    list_el = state.get("_history_list_el")
    if list_el is not None:
        _render_history_list(article_id, state, list_el)


def _format_ts(ts) -> str:
    """A short, display-friendly timestamp (YYYY-MM-DD HH:MM) for a version row, or "" when absent.
    Tolerates a non-datetime by falling back to str()."""
    if ts is None:
        return ""
    try:
        return ts.strftime("%Y-%m-%d %H:%M")
    except Exception:  # pragma: no cover - defensive against odd types
        return str(ts)


async def _save_edits(article_id: str, state: dict, editor_area) -> None:
    """Persist the textarea content to articles.current_draft (the hand-edit path) and refresh the
    preview. This is the owner's direct edit channel — hand-edits are sacred (hard rule), so this
    writes the raw textarea verbatim. The write goes off the event loop via run.io_bound; on
    success the preview re-renders from the new draft and a confirmation notify fires."""
    new_draft = editor_area.value or ""
    await run.io_bound(_persist_draft, article_id, new_draft)
    state["draft"] = new_draft
    _refresh_draft_views(state)
    _refresh_history(article_id, state)
    ui.notify("Saved", type="positive")


def _persist_draft(article_id: str, draft: str) -> None:
    """Blocking core of Save edits (runs in a worker thread): write current_draft + commit.

    A direct, bounded UPDATE of the one column the owner hand-edited — the article already exists
    (the editor view loaded it). Opens its own session, mutates, commits. Never publishes; the
    only column touched is current_draft."""
    from app.db.models import Article

    with _db_session() as session:
        article = session.get(Article, article_id)
        if article is None:
            # Vanishingly unlikely (the page loaded the article), but fail loudly rather than
            # silently dropping the owner's edit.
            raise ValueError(f"article {article_id!r} not found")
        article.current_draft = draft
        session.commit()


def _refresh_draft_views(state: dict) -> None:
    """Re-render the preview (rich: highlighted code + mermaid diagrams) and refresh the raw textarea
    from the current `state["draft"]`. Called after an agent draft or a Save so both panes reflect
    the persisted draft. No-op for the elements that aren't present (defensive)."""
    preview = state.get("_preview_el")
    textarea = state.get("_textarea_el")
    if preview is not None:
        _render_draft_preview(preview, _preview_text(state["draft"]))
    if textarea is not None:
        textarea.value = state["draft"] or ""


def _preview_text(draft: str | None) -> str:
    """The markdown to render in the preview: the draft, or the empty-draft placeholder."""
    return draft if (draft or "").strip() else _EMPTY_DRAFT_PREVIEW


# --- rich draft preview: syntax-highlighted code + mermaid diagrams (Phase 10c) -------------
#
# The draft preview renders markdown with syntax-highlighted fenced code (NiceGUI's `ui.markdown`
# does this out of the box via its default `fenced-code-blocks` extra → Pygments `codehilite`), AND
# renders ```mermaid fenced blocks as actual diagrams via `ui.mermaid`. We split the draft on
# ```mermaid fences ourselves (rather than the markdown `mermaid` extra) so each diagram is its own
# `ui.mermaid` element — clearer routing, and a malformed block falls back to a plain code block
# without taking down the whole preview.

# Matches a ```mermaid fenced block: the opening fence (optionally indented) with the `mermaid` info
# string, the body (captured), and the closing fence. DOTALL so the body can span lines; non-greedy
# so back-to-back diagrams don't merge into one.
_MERMAID_FENCE = re.compile(
    r"^[ \t]*```[ \t]*mermaid[ \t]*\r?\n(.*?)\r?\n[ \t]*```[ \t]*$",
    re.DOTALL | re.MULTILINE | re.IGNORECASE,
)


def _split_mermaid_segments(text: str) -> list[tuple[str, str]]:
    """Split `text` into ordered ("markdown", chunk) / ("mermaid", code) segments by ```mermaid
    fences. The markdown chunks render via `ui.markdown` (with code highlighting); each mermaid chunk
    renders via `ui.mermaid`. Empty markdown chunks (e.g. two adjacent diagrams) are dropped. When
    there is no mermaid fence the whole text is one markdown segment."""
    segments: list[tuple[str, str]] = []
    pos = 0
    for m in _MERMAID_FENCE.finditer(text):
        before = text[pos : m.start()]
        if before.strip():
            segments.append(("markdown", before))
        segments.append(("mermaid", m.group(1)))
        pos = m.end()
    tail = text[pos:]
    if tail.strip() or not segments:
        # Keep the tail (or, when there were no fences at all, the whole text) as a markdown segment.
        segments.append(("markdown", tail))
    return segments


def _render_draft_preview(container, text: str) -> None:
    """(Re-)render the rich draft preview INTO `container` (cleared first), splitting on ```mermaid
    fences: each markdown segment renders as `ui.markdown` (default extras → Pygments-highlighted
    fenced code) and each mermaid segment as `ui.mermaid`. A malformed mermaid block must NOT crash
    the preview — if constructing `ui.mermaid` raises, we fall back to rendering that segment as a
    plain fenced ```mermaid code block via `ui.markdown`. Used everywhere the preview is (re)rendered
    (initial editor load + after a chat iterate / piece switch / save / restore)."""
    container.clear()
    with container:
        for kind, chunk in _split_mermaid_segments(text):
            if kind == "mermaid":
                try:
                    ui.mermaid(chunk).classes("w-full").mark("preview-mermaid")
                except Exception:  # pragma: no cover - defensive: never let one diagram blank the page
                    log.exception("mermaid render failed; falling back to a code block")
                    ui.markdown(f"```mermaid\n{chunk}\n```").classes("w-full")
            else:
                ui.markdown(chunk).classes("w-full")


# --- shared chrome -------------------------------------------------------------------------


def _page_header(title: str, *, crumb: str = "") -> None:
    """Render the shared top bar: a link home + the page title + an optional breadcrumb. Kept tiny
    and dependency-free so every page has consistent chrome without a base template."""
    with ui.header().classes("items-center gap-4 px-4 py-2"):
        ui.link("AI Content Engine", "/").classes("text-white font-semibold no-underline")
        if crumb:
            ui.label(crumb).classes("text-sm opacity-80")


def _not_found(message: str) -> None:
    """Render a themed not-found page (used when an article id doesn't exist). A message + a link
    home, matching the old not_found template's shape."""
    _page_header("Not found", crumb="404")
    with ui.column().classes("max-w-3xl mx-auto p-6 gap-3").mark("not-found"):
        ui.label("Not found").classes("text-lg font-semibold")
        ui.label(message)
        ui.link("← back to dashboard", "/")


# Register the pages at import time so a plain `import app.web.ui_pages` (or importing the package)
# wires them onto the global NiceGUI app. Guarded so re-import / re-exec (e.g. the test harness'
# runpy of the main file) doesn't double-register and raise.
_REGISTERED = False


def ensure_registered() -> None:
    """Register the pages exactly once. Safe to call repeatedly (routes import, test main file)."""
    global _REGISTERED
    if _REGISTERED:
        return
    register_pages()
    _REGISTERED = True


ensure_registered()


__all__ = ["register_pages", "ensure_registered"]
