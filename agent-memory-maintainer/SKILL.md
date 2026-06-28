---
name: agent-memory-maintainer
description: 维护 agent_memory 这个紧凑的上下文工程记忆系统。当 Codex 需要创建、更新、查阅、路由、抽取、巩固或刷新 agent_memory/ 记录时使用，覆盖当前上下文、长期知识、命令、已解决案例和成熟 playbook。只把 agent_memory/ 作为目标记忆系统。
---

# Agent Memory 维护器

把 `agent_memory/` 维护成给后续 agent 使用的、已验证的长期上下文记忆。它不是聊天记录归档，而是帮助下一次运行用最少阅读量重建正确上下文。

## 核心结构

新的 V2 记忆系统使用下面的结构：

```text
agent_memory/
  README.md                 # 记忆协议和写入规则
  INDEX.md                  # 范围路由

  common/
    context.md              # 范围边界 + 短期工作台
    knowledge.md            # 长期事实 + 决策
    commands.md             # 可复跑命令记忆
    cases.md                # 已解决或边界明确的问题
    playbooks.md            # 可选：成熟流程

  modules/
    <module>/
      <function>/
        context.md
        knowledge.md
        commands.md
        cases.md
        playbooks.md        # 可选
```

不要创建空的可选文件。只有某个范围已经有成熟、可复用的程序性记忆时，才创建 `playbooks.md`。

## 记忆类型

- `context.md`：会话记忆加范围边界。记录当前目标、已验证边界、阻塞、下一步、开放风险和过期条件。它是短期工作台，不是长期事实。
- `knowledge.md`：语义记忆。记录稳定事实、路径、模块关系、环境事实、长期约束、已确认决策、拒绝方案和被替代结论。
- `commands.md`：命令记忆。记录 host、board、CI 或 service 上可复跑的命令，包括 cwd、环境、完整命令、成功信号、失败信号和最近验证信息。
- `cases.md`：情景/案例记忆。记录已解决或边界明确的问题，包括现象、证据、根因、修复或规避、验证和防回归。
- `playbooks.md`：程序性记忆。记录从多次案例或已验证操作中提炼出的成熟流程，包括触发条件、完成条件、反馈循环、分支和停止/升级规则。

默认把 `cases.md` 和 `playbooks.md` 保持为单文件。只有文件已经大到难以扫描、某类案例需要独立索引，或某个 playbook 有大量分支和验证矩阵时，才拆成目录。

## 读取流程

处理可能依赖记忆的任务前：

1. 先读仓库级说明，例如存在时读取 `AGENTS.md`。
2. 读 `agent_memory/README.md`，确认记忆协议。
3. 读 `agent_memory/INDEX.md`，选择最窄的相关范围。
4. 在选中的范围内，按顺序读：`context.md`、`knowledge.md`、存在时读 `playbooks.md`、再读 `commands.md` 和相关 `cases.md`。
5. 优先使用当前、已验证、窄范围的记录。除非是在查历史或冲突原因，否则不要默认注入宽泛、过期、`superseded`、`expired` 或低置信度记录。

## 写入生命周期

每次记忆更新都按下面流程处理：

```text
Retrieve -> Execute -> Extract -> Classify -> Consolidate -> Store -> Promote / Expire
```

- `Retrieve`：写入前先读取相关 V2 范围。
- `Execute`：收集真实反馈，例如命令输出、日志、测试结果、构建结果、板端信号、截图、diff、文件内容或用户明确确认。
- `Extract`：只抽取未来有用、值得长期保留的候选记忆。不要复制聊天流水账或原始日志。
- `Classify`：判断候选记忆应该归为当前上下文、长期知识、命令、案例，还是 playbook 素材。
- `Consolidate`：写入前先和已有记录对照。重复的合并，冲突的事实替换，过时记录标为 `superseded` 或 `expired`，无法验证的信息只放进 `context.md` 的开放风险。
- `Store`：把最小必要内容写到最窄范围。
- `Promote / Expire`：把多次验证的案例经验提升到 `playbooks.md`；过期的上下文和旧流程要淘汰或标记过期。

## 主记录位置

对需要长期保存的候选信息，先判断它的主记录位置。同一条可维护信息只在一个文件里维护完整细节；其他文件可以保留短摘要或引用，但不要重复维护同一事实、命令全文、案例细节或流程步骤。

主记录位置按记忆类型决定：

- `context.md` 维护当前目标、阻塞、下一步、开放风险和过期条件。
- `knowledge.md` 维护稳定事实、环境边界、长期约束和决策。
- `commands.md` 维护完整可复跑命令、执行侧、cwd、环境、成功信号和失败信号。
- `cases.md` 维护已解决或边界明确的问题、证据、根因、修复、验证和防回归。
- `playbooks.md` 维护从多个案例或命令提炼出的流程、分支、反馈循环和停止/升级规则。

case 提升为 playbook 时，只抽象可复用流程；不要复制单个案例的完整根因、日志或命令全文。playbook 使用命令或案例时，引用对应标题即可。小更新可以直接按文件职责落位；大迁移或多条记录重组时，先列出候选信息和主记录位置，再写入。

## 放置规则

- 跨模块事实、用户偏好、板端访问、公共构建/部署命令和跨模块常见问题放到 `common/`。
- 模块/功能专属状态放到 `modules/<module>/<function>/`。
- 模块或功能归属不清时，先问用户，不要直接创建新范围。
- 请求匹配已有范围时，复用最接近的范围；不要为同一工作创建多个名字不同的重复范围。
- 新建、重命名范围，或某个范围成为推荐入口时，同步更新 `INDEX.md`。
- 范围边界、相关范围、当前状态或过期条件变化时，同步更新 `context.md`。

## 范围判定

默认更新已有范围。只有长期记忆边界确实不同，才新建 `modules/<module>/<function>/`。

更新已有范围的典型情况：

- 目标源码、包、二进制、板端路径或验证命令仍是同一组。
- 只是同一功能下的新 bug、新命令、新约束、新验证或新案例。
- 新信息会让后续 agent 更好理解同一个 `context.md`，而不是需要另一个入口。
- 命令、案例和 playbook 仍属于同一条验证链。

新建范围的典型情况：

- 产物、入口程序、运行环境或板端部署路径不同。
- 成功信号、失败信号、回归门槛或停止条件明显不同。
- 两类任务放在一起会让 `context.md` 变成混合入口。
- 同一模块下已经分裂出独立功能，后续 agent 需要从不同入口开始读。

跨多个模块都适用的信息放到 `common/`，不要塞进某个 module/function。不确定时先问用户。

## 记录元数据

后续可能被检索的记录使用紧凑元数据：

```markdown
## <具体标题>
> type: context | fact | decision | command | case | playbook
> status: candidate | current_verified | superseded | expired
> confidence: high | medium | low
> last_verified: <日期、命令、commit、日志、板端信号或用户确认>
> evidence: <简短证据指针>
> stale_when: <过期条件，未知可省略>
> related: <相关记录或路径，可选>
```

`candidate` 只用于有价值但尚未完全验证的信息。候选内容应放在 `context.md`，或在记录里明确标注，不能伪装成稳定事实。

## 文件模板

`README.md` 应该短而稳定：

```markdown
# Agent Memory 记忆

## 用途
给后续 agent 使用的长期上下文记忆。不是聊天记录归档。

## 读取顺序
AGENTS.md -> agent_memory/README.md -> INDEX.md -> 目标范围内的 context 和记忆文件。

## 写入规则
先抽取、分类、巩固，再写入最小的已验证记录。
```

`INDEX.md` 负责路由，不写叙事：

```markdown
# Agent Memory 索引

| 领域 | 范围 | 起点 | 说明 |
| --- | --- | --- | --- |
| 公共板端/构建/用户规则 | common | common/context.md | 跨模块 |
| <module/function> | modules/<module>/<function> | modules/<module>/<function>/context.md | <reason> |
```

`context.md` 合并范围边界和当前工作台：

```markdown
# 上下文

## 范围
这个范围覆盖什么、不覆盖什么、相关范围在哪里。

## 当前目标

## 已验证边界

## 阻塞

## 下一步

## 开放风险

## 过期条件
```

`knowledge.md` 合并长期事实和决策：

```markdown
# 知识

## 稳定事实

## 决策和约束

## 已替代 / 已过期
```

`commands.md` 记录可精确复跑的命令：

````markdown
## <命令用途>
> type: command
> status: current_verified
> last_verified: <证据>

**执行侧：** host | board | CI | service
**cwd：** `<path>`
**环境：** `<环境变量或前置条件>`
**命令：**
```bash
<完整命令>
```
**成功信号：** <可观察的通过条件>
**失败信号：** <已知失败信号>
````

`cases.md` 记录已解决或边界明确的问题：

```markdown
## <现象或问题>
> type: case
> status: current_verified
> last_verified: <证据>

**问题：** <可观察的问题和影响范围>
**证据：** <日志、命令、文件、板端信号、diff 或用户确认>
**根因：** <已验证根因>
**修复：** <修复方式或规避方式>
**验证：** <证明已生效的证据>
**防回归：** <如何避免或识别复发>
**提升：** <是否需要更新 knowledge、commands 或 playbooks>
```

`playbooks.md` 只在已有成熟流程时创建：

```markdown
## <流程名称>
> type: playbook
> status: current_verified
> last_verified: <证据>

**触发：** <什么时候使用>
**完成条件：** <完成前必须拿到的真实反馈>
**所需上下文：** <开始前要读的文件、记忆记录、日志、板端状态或源码路径>
**流程：** <有序步骤>
**反馈循环：** <如何根据证据继续、分支、重试或停止>
**分支：** <常见变体>
**停止 / 升级：** <失败次数、重复错误、权限不足或成本限制>
**命令引用：** <指向 commands.md 记录的链接>
**相关案例：** <指向 cases.md 记录的链接>
```

## 质量门槛

完成记忆更新前检查：

- 目标范围明确；如果是新范围，已经从 `INDEX.md` 链接过去。
- `context.md` 内的当前工作台状态和长期知识明确分开。
- `knowledge.md` 内的事实和决策明确分开。
- 命令、案例和 playbook 没有混写。
- 需要长期保存的信息有清晰主记录位置；其他文件没有重复维护同一细节。
- case 提升为 playbook 时只抽象流程，没有复制案例正文或命令全文。
- 命令包含精确 cwd、执行侧、命令文本、成功信号和失败信号。
- 案例包含证据、根因、修复、验证和防回归。
- playbook 包含触发条件、完成条件、反馈循环和停止/升级规则。
- 新记录已经和旧记录做过巩固；冲突已经解决或标记。
- 未验证猜测被标为风险或候选项，没有伪装成稳定事实。
- 没有写入密钥、token、密码、私钥、cookie 或解码后的秘密值。
