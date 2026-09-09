---
company: NVIDIA
title: "Introducing CUDA Rust: Two Tracks for Writing GPU Kernels"
url: https://developer.nvidia.com/blog/introducing-cuda-rust-two-tracks-for-writing-gpu-kernels
published: 2026-09-08
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-09
---

NVIDIA introduces CUDA Rust, letting developers write GPU kernels natively in Rust (compiled to PTX) rather than only launching kernels written elsewhere — via two open-source tracks: cuda-oxide (SIMT, alpha, nightly Rust) and cutile-rs (tile-based, stable Rust 1.89+, already used in HuggingFace's Grout and mistral.rs).

## card

**Що сталося:** NVIDIA представила CUDA Rust — можливість писати GPU-ядра (kernels) напряму на Rust з компіляцією в PTX, а не лише запускати ядра, написані іншими мовами. Реалізовано у вигляді двох окремих треків з різними компромісами.

**Контекст:** Раніше Rust міг лише запускати CUDA-ядра, написані на інших мовах — можливості писати самі ядра нативно на Rust не було. Обидва треки — open-source і доступні вже зараз; NVIDIA планує розвивати CUDA Rust протягом 2027 року і далі.

**Деталі:**
- **cuda-oxide** (SIMT-трек): власний codegen-бекенд для rustc, шлях Rust MIR → Pliron IR → LLVM → PTX; альфа-стадія, потребує закріпленого nightly-тулчейну та системного LLVM; безпека пам'яті через тип `DisjointSlice` та launch contracts
- **cutile-rs** (tile-трек): вищий рівень абстракції (tile-based), JIT-компіляція через CUDA Tile IR; працює на стабільному Rust 1.89+ з CUDA 13.3, без nightly чи кастомного LLVM; вже опубліковано на crates.io та використовується у Grout (HuggingFace) і mistral.rs
- Обидва треки потребують GPU з compute capability 8.0+
- Заплановано міжмовну сумісність між CUDA Rust, C++ і Python
- Жоден з проєктів ще не production-ready; cutile-rs просунутіший
