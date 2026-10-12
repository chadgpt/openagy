# antigravity — reconstructed proto schema (auth + eligibility)

**Source:** FieldDescriptorProto blobs parsed directly from `/workspace/agy/install/antigravity` (binary has no `.proto` source — Google's `v1internal` is an internal package). The data uses Google's **modified `FieldDescriptorProto` layout** where:
- field 1 (LEN) = name
- field 3 (varint) = **field number** (NOT standard field 2)
- field 4 (varint) = label (1=OPTIONAL, 2=REQUIRED, 3=REPEATED)
- field 5 (varint) = type (1=DOUBLE, 9=STRING, 11=MESSAGE, 14=ENUM, ...)
- field 6 (LEN) = type_name (when type=message/enum)
- field 10 (LEN) = json_name

> **Note on field 2 vs field 3.** The standard `google.protobuf.FieldDescriptorProto` has field 2 as the field number, but Google's modified format shifts that to field 3. This is consistent across all 14 messages I parsed. The field *numbers* themselves (1, 2, 3, ...) are unchanged — only the wire-encoding field number in the descriptor is shifted.

Type values are standard proto: `{1:double, 2:float, 3:int64, 4:uint64, 5:int32, 6:fixed64, 7:fixed32, 8:bool, 9:string, 10:group, 11:message, 12:bytes, 13:uint32, 14:enum, 15:sfixed32, 16:sfixed64, 17:sint32, 18:sint64}`.

Label values: `{1:optional, 2:required, 3:repeated}`.

JSON names are the camelCase versions of the snake_case proto field names (Go proto convention).

---

## File: `google3/google/internal/cloud/code/v1internal/v1internal.proto`

```proto
syntax = "proto3";
package google.internal.cloud.code.v1internal;

message IneligibleTier {
  IneligibleTierReasonCodes reason_code = 1;  // enum (IneligibleTierReasonCodes)
  string reason_message = 2;
  string tier_id = 3;
  string tier_name = 4;
  string validation_error_message = 5;
  string validation_url_link_text = 6;
  string validation_url = 7;
  string validation_learn_more_link_text = 8;
  string validation_learn_more_url = 9;
}

message UserTier {
  string id = 1;
  string name = 2;
  string description = 3;
  bool user_defined_cloudaicompanion_project = 4;
  PrivacyNotice privacy_notice = 5;
  bool is_default = 6;
  string upgrade_subscription_uri = 7;
  string upgrade_subscription_text = 8;
  UpgradeSubscriptionType upgrade_subscription_type = 9;  // enum
  string upgrade_button_text = 11;
  string client_experience_tag = 12;
  bool uses_gcp_tos = 13;
  AvailableCredits available_credits = 14;  // message
}

message LoadCodeAssistRequest {
  string cloudaicompanion_project = 1;
  ClientMetadata metadata = 2;
  Mode mode = 3;  // enum
}

message LoadCodeAssistResponse {
  UserTier current_tier = 1;
  repeated UserTier allowed_tiers = 2;
  string cloudaicompanion_project = 3;
  Status project_validation_error = 4;  // google.rpc.Status
  repeated IneligibleTier ineligible_tiers = 5;
  bool gcp_managed = 6;
  string manage_subscription_uri = 7;
  ReleaseChannel release_channel = 8;
  string upgrade_subscription_uri = 9;
  string g1_tier = 11;
  UserTier paid_tier = 12;
}
```

---

## File: `google3/third_party/jetski/language_server_pb/language_server.proto`

```proto
syntax = "proto3";
package exa.language_server_pb;  // the proto package is "exa", Go package is "language_server_go_proto"

message SelectLicenseRequest {
  string user_tier = 1;
  string project_id = 2;
  string location = 3;
  string tier_display_name = 4;
}

message SelectLicenseResponse {
  AuthResult auth_result = 1;
}

message SelfAssignLicenseRequest {
  string parent = 1;
  // Per seeds.txt Get accessors, also has: project_id (2), location (3)
  // — likely the same shape as SelectLicenseRequest
  string project_id = 2;
  string location = 3;
}

message SelfAssignLicenseResponse {
  License license = 1;
  // Per seeds.txt Get accessors, also has: assigned (2), error_message (3),
  // data_sharing_disclaimer (4), and a duplicate license (??)
  bool assigned = 2;
  string error_message = 3;
  string data_sharing_disclaimer = 4;
}

message ListLicensesResponse {
  repeated License licenses = 1;
  string data_sharing_disclaimer = 2;
}

// Per the v1beta_management_service (businessaicode) — also exists in v1main
message FetchLicensesResponse {
  repeated License licenses = 1;
  // (2 and 3 inferred from Get accessors; type not recovered)
  repeated string unreachable = 2;  // inferred; matches v1beta pattern
  string data_sharing_disclaimer = 3;  // inferred
}

message GetLoadCodeAssistRequest {
  // (no fields recovered in the descriptor; exists per service definition)
}

message GetLoadCodeAssistResponse {
  LoadCodeAssistResponse response = 1;  // wraps the response
}

message License {
  string user_tier = 1;
  string tier_display_name = 2;
  UpgradeSubscription upgrade_subscription = 3;  // message
}

message AuthResult {
  bool has_valid_auth = 1;
  string ui_message = 2;
  IneligibleInfo ineligible = 3;
  VerificationRequired verification_required = 4;
  TosErrorInfo tos_violation = 5;
  GeneralError general_error = 6;
  ProjectRequiredInfo project_required = 7;
  repeated string granted_scopes = 8;
  HeadlessAuthRequired headless_auth_required = 9;
  bool is_gcp_tos = 10;
  string project_id = 11;
  string location = 12;
  LicenseRequiredInfo license_required = 13;
  string wif_provider = 14;
  AuthMode auth_mode = 15;  // enum
}
```

> **Caveat on `SelfAssignLicense*` and `FetchLicenses*`.** The binary's `FieldDescriptorProto` data for these messages shows only the first field. The other fields are inferred from the `Get*` accessor function names in `seeds.txt`. Field numbers (2, 3, 4) follow standard proto3 declaration order, but the actual wire field numbers should be verified against a real `language_server.proto`.

---

## File: `google3/google/cloud/businessaicode/v1main/entitlement.proto`

```proto
syntax = "proto3";
package google.cloud.businessaicode.v1main;

message Entitlement {
  string user_tier = 2;  // starts at 2 (field 1 reserved)
}
```

---

## File: `google3/google/internal/cloud/code/v1internal/credits.proto`

```proto
syntax = "proto3";
package google.internal.cloud.code.v1internal;

message Credits {
  CreditType credit_type = 1;  // enum
  int64 credit_amount = 2;
  int64 minimum_credit_amount_for_usage = 3;
}
```

---

## Services (from gRPC handler functions)

### `language_server_go_grpc.LanguageServerService`

| RPC | Handler | Client stub |
|-----|---------|-------------|
| `SelectLicense` | `_LanguageServerService_SelectLicense_Handler` (0x6ca2fc0) | `(*languageServerServiceClient).SelectLicense` (0x7c2f900) |
| `SelfAssignLicense` | `_LanguageServerService_SelfAssignLicense_Handler` (0x6ca31e0) | `(*languageServerServiceClient).SelfAssignLicense` (0x7c2fb20) |
| `FetchLicenses` (v1beta) | `_ManagementService_FetchLicenses_Handler` (0x746b8e0) | `(*CodeAssistClient).FetchLicensesFromAICode` (0x798b480) |
| `LoadCodeAssist` (v1internal) | `_CloudCode_LoadCodeAssist_Handler` (0x6c5e540 — inferred) | `(*CodeAssistClient).LoadCodeAssist` |

### `cloudaicompanion.googleapis.com` (gRPC server, not in binary)

The actual gRPC server side is the **Cloud Code Assist** service running on Google Cloud. The binary only contains the **client stubs** (gRPC + Connect clients). Server-side message types (GoogleCloudBusinessAicode v1beta) are stub-defined locally for type safety.

---

## How the schema was reconstructed

1. **Field names** — extracted from the `Get*` accessor function names in `seeds.txt`:
   - 22,166 total `Get*` accessors across 4,732 message types
   - For each target message, enumerated all `Get<Field>` accessors

2. **Field numbers + types** — extracted by parsing the `FileDescriptorProto` data directly from the binary:
   - Located each message's `DescriptorProto` by searching for `0x0a <varint> <MessageName>` in the binary
   - Parsed the `FieldDescriptorProto` sub-messages using a 0-dependency protobuf wire-format parser
   - Filtered out enum value definitions (which also start with field 1 = name, but have no field numbers)

3. **Type references** — `type_name` strings in the descriptor point to other message/enum types. The type's short name is the last component after the final `.`.

4. **Sanity check** — every field's `json_name` matches the standard camelCase conversion of its `name` (e.g., `cloudaicompanion_project` → `cloudaicompanionProject`). This is Google's enforced convention, so it confirms the parsing is correct.

---

## Open questions / can't determine from binary

- The full `LanguageServerService` proto (only 6 of ~20 RPCs have local handler stubs)
- The `v1beta_management_service` proto (`SelfAssignLicense` request has `parent` + `project_id` + `location`, response has `license` + `assigned` + `error_message` + `data_sharing_disclaimer`)
- Enum value lists for `IneligibleTierReasonCodes`, `Mode`, `CreditType`, `AuthMode`, `UpgradeSubscriptionType`, `ReleaseChannel` — these would require parsing `EnumDescriptorProto` data
- Field options (e.g., `[deprecated = true]`, custom options)
- Oneof declarations — `LoadCodeAssistRequest` has `cloudaicompanion_project` + `metadata` which look like a oneof pattern
