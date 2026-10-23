# Experiment 009 — simulated LED displays

Status: **active — architecture and first LCD vertical slice**

Tracking issue: [brainboxemb.meta #188](https://github.com/brainboxemb/brainboxemb.meta/issues/188)

Implementation and evidence: [exp.2026-009.simulated-display](https://github.com/brainboxemb/exp.2026-009.simulated-display)

## Question

Can the same C display interpretation and rendering core operate on a host and an ESP32 while a JavaFX simulator accurately displays the native output?

## Reference displays

| Mode | Resolution | Colour | Input | Rendering |
| --- | --- | --- | --- | --- |
| Small LED display | 90 × 35 | Monochrome red | SparkFun Serial Graphic LCD-style byte stream | Built-in 5×7 glyphs, 6×8 cells, graphics in C |
| HUB75 | 160 × 64; five panels | RGB | Synchronized application data and own interpretation | Native renderer, optionally LVGL |

The target LCD is a red LED matrix, not a physically faithful SparkFun LCD. SparkFun command compatibility should be assessed explicitly against the published protocol.

## Target design

```text
LCD serial bytes / HUB75 synchronized data
                  |
           C interpreter
                  |
         C glyph / graphics renderer
                  |
          logical framebuffer
                  |
       platform-independent flush
             /             \
     desktop host        ESP-IDF/HUB75
          |
     JavaFX simulator
```

Java 21 / JavaFX 21, Maven and NetBeans are the desktop baseline; C11 and CMake are the native baseline. The Java frontend must not implement the protocol or character glyphs. Both variants share rendering/output principles but are free to have different parsers and pixel formats. Neither Arduino nor libuv is a baseline dependency. Evaluate LVGL for HUB75 after the small core works. Allow a thin hardware-driver C ABI adapter if an ESP-IDF driver is implemented in C++.

## PoP sequence

1. LCD: native monochrome framebuffer, 5×7 ASCII font, streaming serial parser, cursor and clear, set/reset pixels and a basic desktop native-to-JavaFX pixel transport.
2. Qualify byte-chunk independence, cursor behaviour, clipping, font pixels and byte protocol against a reference; extend drawing commands according to documented semantics.
3. HUB75: logical 160×64 RGB framebuffer, five-panel visualization, native synchronized-data interpreter and LVGL evaluation.
4. ESP32: compile reusable C code under ESP-IDF, prove driver boundary and verify physical panel order on real hardware when available.
5. Record exact source/tests, limitations and a decision on reusable architecture and production ownership.

## Ownership and completion

`brainboxemb.meta` owns the cross-project question, status, evidence summary and later production handoff. `exp.2026-009.simulated-display` owns source, architecture details, fixtures and reproducible test evidence. A successful experiment does not itself start production adoption. No PoP success is claimed yet.
