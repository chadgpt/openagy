## evidence_id

ev_fff4e55ad44ac41ba92e1e0a434f12922d4f207d8f726e6cc18240620c9045d9

## subject.name

antigravity

## subject.digest

| Key    | Value                                                            |
|--------|------------------------------------------------------------------|
| sha256 | d97edcf90eda1799cd6cedc92616ef402f23c9752a723e8b8ae3e8f062ce458b |

## subject.format

elf

## subject.architecture

null

## subject.local_path

/run/csi/mount-root/nas/eab0d61a99b6696edb3d2aff87b585e8/agy/install/antigravity

## provider

| Key     | Value                            |
|---------|----------------------------------|
| id      | rea-artifact-graph               |
| name    | REA safe artifact graph provider |
| version | 1                                |

## analysis_profile

null

## predicate_type

rea.analysis

## operation

inspect_artifact

## parameters

| Key              | Value |
|------------------|-------|
| integrity_policy | fail  |

## raw_result

null

## normalized_result.inspection_id

ai_03acfcee684292d5d97005d623b0b41a3d1876927478b6219cb469b67eeaf4ec

## normalized_result.subject

| Key              | Value                                                                |
|------------------|----------------------------------------------------------------------|
| manifest_id      | agm_ee9a89c7ea9b308ade32c989e89dce9dc3e6f4df8015dab6cd6ec144b2ba9b6b |
| root_artifact_id | art_27ab53f132b69d9a8d33c8c0134b05605d3abe054cf1777d7e7fb9b112a0e997 |
| root_sha256      | d97edcf90eda1799cd6cedc92616ef402f23c9752a723e8b8ae3e8f062ce458b     |
| root_format      | elf                                                                  |

## normalized_result.substeps

| substep_id                                                           | operation          | status    | evidence_id                                                         | evidence        |
|----------------------------------------------------------------------|--------------------|-----------|---------------------------------------------------------------------|-----------------|
| ais_e07b74a870ee84e11f16f348753c1a7bd71b740eae1acf6648045c611a13ea67 | inventory_artifact | completed | ev_af106c9353df665068142cc9b0672699df3fc514c70ee18e611cd28284e0a8e2 | [object Object] |

## normalized_result.observations

| observation_id                                                       | kind          | subject                                                              | value           | evidence_id                                                         |
|----------------------------------------------------------------------|---------------|----------------------------------------------------------------------|-----------------|---------------------------------------------------------------------|
| aio_0d0ec07b3c1aa61f9a1518ef805e68dc360b63a4b68183fadae338b79768bd70 | root-manifest | art_27ab53f132b69d9a8d33c8c0134b05605d3abe054cf1777d7e7fb9b112a0e997 | [object Object] | ev_af106c9353df665068142cc9b0672699df3fc514c70ee18e611cd28284e0a8e2 |

## normalized_result.hypotheses



## normalized_result.contradictions



## normalized_result.unexplored_branches

| branch_id                                                            | reason                            | detail                                                           | next_probe      | evidence_id                                                         |
|----------------------------------------------------------------------|-----------------------------------|------------------------------------------------------------------|-----------------|---------------------------------------------------------------------|
| aib_b96a4bde256443c7ca731a9d9503d8b17bd14df567b7c33b964446a56c29826f | format-specific-analysis-required | open_binary was not run by provider-neutral artifact inspection. | [object Object] | ev_af106c9353df665068142cc9b0672699df3fc514c70ee18e611cd28284e0a8e2 |

## normalized_result.next_probes

| operation   | rationale                                                     | authority                |
|-------------|---------------------------------------------------------------|--------------------------|
| open_binary | Bind one deep native provider before function-level analysis. | native-analysis-provider |

## normalized_result.coverage

| Key                          | Value                    |
|------------------------------|--------------------------|
| status                       | complete-within-substeps |
| substeps_completed           | 1                        |
| observations_retained        | 1                        |
| observations_omitted         | 0                        |
| hypotheses_retained          | 0                        |
| hypotheses_omitted           | 0                        |
| unexplored_branches_retained | 1                        |
| unexplored_branches_omitted  | 0                        |
| next_probes_retained         | 1                        |
| next_probes_omitted          | 0                        |

## normalized_result.evidence_links

ev_af106c9353df665068142cc9b0672699df3fc514c70ee18e611cd28284e0a8e2

## normalized_result.limitations

Artifact has no child container entries.,Inspection derives bounded static hypotheses and next probes; it does not execute the artifact or claim format-specific semantics.

## confidence

observed

## authority

shipped-artifact

## environment

null

## limitations

Artifact has no child container entries.,Inspection derives bounded static hypotheses and next probes; it does not execute the artifact or claim format-specific semantics.

## locations



## evidence_links

ev_af106c9353df665068142cc9b0672699df3fc514c70ee18e611cd28284e0a8e2
