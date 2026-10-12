# Decompile report — `google3/third_party/jetski/cli/printmode/printmode.`

> 36 priority functions in this Go package

**Decompiled:** 20/36

## `google3/third_party/jetski/cli/printmode/printmode.(*AgentError)`

_2 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8c690c0` | `google3/third_party/jetski/cli/printmode/printmode.(*AgentError).Error` |  | |
| `0x8c690e0` | `google3/third_party/jetski/cli/printmode/printmode.(*AgentError).structuredLine` |  | |

## `google3/third_party/jetski/cli/printmode/printmode.(*StreamInputUserMessage)`

_1 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8c6d360` | `google3/third_party/jetski/cli/printmode/printmode.(*StreamInputUserMessage).PromptText` | **yes** | |

## `google3/third_party/jetski/cli/printmode/printmode.(*jsonEmitter)`

_3 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8c57360` | `google3/third_party/jetski/cli/printmode/printmode.(*jsonEmitter).BeginTurn` |  | |
| `0x8c57680` | `google3/third_party/jetski/cli/printmode/printmode.(*jsonEmitter).HasResponse` |  | |
| `0x8c57700` | `google3/third_party/jetski/cli/printmode/printmode.(*jsonEmitter).emitJSON` |  | |

## `google3/third_party/jetski/cli/printmode/printmode.(*session)`

_8 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8c6bbe0` | `google3/third_party/jetski/cli/printmode/printmode.(*session).warnUnsandboxed` |  | |
| `0x8c6bce0` | `google3/third_party/jetski/cli/printmode/printmode.(*session).close` |  | |
| `0x8c6bd20` | `google3/third_party/jetski/cli/printmode/printmode.(*session).Snapshot` |  | |
| `0x8c6bd80` | `google3/third_party/jetski/cli/printmode/printmode.(*session).HeadlessDenials` |  | |
| `0x8c6bdc0` | `google3/third_party/jetski/cli/printmode/printmode.(*session).start` |  | |
| `0x8c6c040` | `google3/third_party/jetski/cli/printmode/printmode.(*session).emitInit` |  | |
| `0x8c6c1c0` | `google3/third_party/jetski/cli/printmode/printmode.(*session).runTurn` |  | |
| `0x8c6df60` | `google3/third_party/jetski/cli/printmode/printmode.(*session).handleStreamMessage` |  | |

## `google3/third_party/jetski/cli/printmode/printmode.(*streamJSONEmitter)`

_2 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8c57c40` | `google3/third_party/jetski/cli/printmode/printmode.(*streamJSONEmitter).BeginTurn` |  | |
| `0x8c57e00` | `google3/third_party/jetski/cli/printmode/printmode.(*streamJSONEmitter).EmitFinal` |  | |

## `google3/third_party/jetski/cli/printmode/printmode.(*textEmitter)`

_4 methods decompiled._

| Addr | Function | Auth-relevant | Notes |
|---|---|---|---|
| `0x8c57060` | `google3/third_party/jetski/cli/printmode/printmode.(*textEmitter).ControlWriter` |  | |
| `0x8c57080` | `google3/third_party/jetski/cli/printmode/printmode.(*textEmitter).EmitInit` |  | |
| `0x8c570a0` | `google3/third_party/jetski/cli/printmode/printmode.(*textEmitter).BeginTurn` |  | |
| `0x8c57200` | `google3/third_party/jetski/cli/printmode/printmode.(*textEmitter).EmitError` |  | |

## Pending / errors (16)

Functions that did not decompile (likely thunks, glue, or out-of-spec):

- `0x8c56fa0` — `google3/third_party/jetski/cli/printmode/printmode.(*textEmitter).EmitStepUpdate`
- `0x8c572a0` — `google3/third_party/jetski/cli/printmode/printmode.(*textEmitter).EmitFinal`
- `0x8c572c0` — `google3/third_party/jetski/cli/printmode/printmode.(*textEmitter).HasResponse`
- `0x8c572e0` — `google3/third_party/jetski/cli/printmode/printmode.(*jsonEmitter).EmitStepUpdate`
- `0x8c57320` — `google3/third_party/jetski/cli/printmode/printmode.(*jsonEmitter).ControlWriter`
- `0x8c57340` — `google3/third_party/jetski/cli/printmode/printmode.(*jsonEmitter).EmitInit`
- `0x8c57380` — `google3/third_party/jetski/cli/printmode/printmode.(*jsonEmitter).EmitError`
- `0x8c57520` — `google3/third_party/jetski/cli/printmode/printmode.(*jsonEmitter).EmitFinal`
- `0x8c57900` — `google3/third_party/jetski/cli/printmode/printmode.(*streamJSONEmitter).EmitStepUpdate`
- `0x8c57b20` — `google3/third_party/jetski/cli/printmode/printmode.(*streamJSONEmitter).ControlWriter`
- `0x8c57b40` — `google3/third_party/jetski/cli/printmode/printmode.(*streamJSONEmitter).EmitInit`
- `0x8c57c60` — `google3/third_party/jetski/cli/printmode/printmode.(*streamJSONEmitter).EmitError`
- `0x8c57f60` — `google3/third_party/jetski/cli/printmode/printmode.(*streamJSONEmitter).HasResponse`
- `0x8c57fe0` — `google3/third_party/jetski/cli/printmode/printmode.(*streamJSONEmitter).emitResult`
- `0x8c58140` — `google3/third_party/jetski/cli/printmode/printmode.(*streamJSONEmitter).emit`
- `0x8c6e7e0` — `google3/third_party/jetski/cli/printmode/printmode.(*session).runStreamTurn`

See `/workspace/agy/out/decompile/dec/_errors.txt` for details.
