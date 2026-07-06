# 嵌入式休眠唤醒检查清单

仅当问题涉及嵌入式系统、kernel driver、suspend/resume、wakeup、power domain、pinctrl、regulator、clock、firmware 或板级硬件时使用本参考。

## 边界分层

- 优先建立最低层可靠红/绿信号；如果 bus-level 或 kernel-level 命令能证明症状，不要从应用 daemon 开始。
- 若平台支持，修改驱动前先对比 `s2idle` 和 `deep`。
- 若平台支持，使用 `pm_test` 分层，把 Linux device suspend/resume 和真正低层 suspend entry 分开。
- 对比 runtime state、源码 device tree、已加载模块、boot image、firmware version 和当前硬件状态。

## 硬件与板级状态

- 假设 firmware 丢失前，先确认 reset、enable、regulator、clock、32 KHz、wake、host-wake 等信号。
- 确认相关 pin 属于哪个 IO domain 或 pinctrl include file。
- 检查 `regulator-state-mem`、power-domain state、`wakeup-source` 使用和 IO retention 设置。
- 把“电源存在”和“IO 状态保持”当成两个不同命题分别验证。

## 驱动与固件

- 区分普通 driver suspend/resume、bus link loss、firmware loss 和 controller reset。
- unbind/bind、reprobe、firmware reload、service restart 或 delay 首先只能作为恢复证据，不是 root cause 证明。
- 如果 workaround 在 resume 后重新初始化硬件，记录它重建了什么状态，以及它没有证明什么。

## 最小验证

- suspend 前后都运行原始红/绿命令。
- 除非修复本身明确要改变相邻子系统，否则最终验证前恢复 WiFi、display、USB 或其它相邻子系统。
- 删除临时 `wakeup-source`、`regulator-on-in-suspend`、module blacklist、debug delay 或 forced reprobe 设置，除非它们就是已验证的最小修复。
