# Project Versioning

## English

Owner decision: 2026-10-10. This policy governs future releases of this repository.

### Release Unit and Contract

Media Manager application; library/database formats, media file operations, configuration, installer and update behavior.

### Version Source and Transition

Authoritative version: `src/version.py::__version__`. The observed source value on 2026-10-10 is `0.0.4`. This policy commit leaves the runtime value unchanged and does not publish a new application release.

Published history includes `v0.0.4.1`, while main currently reports `0.0.4`. Preserve both facts and all old assets. The first new compatible-fix release after that legacy four-part release is `0.0.5`; features or incompatibilities use `0.1.0` or the higher version required by the contract. Do not reinterpret `0.0.4.1` as build metadata or republish `0.0.4`. Check the existing updater against the legacy four-part identity before shipping. The current updater parses numeric versions and does not implement full SemVer prerelease/build-metadata ordering. Keep automatic updates on stable numeric releases until that consumer is updated and tested.

Release tag pattern: `vX.Y.Z` (for example `v1.2.3`). The prefix is not part of the SemVer value.

### Version rules

Use [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html): `MAJOR.MINOR.PATCH`, without leading zeroes. For versions `1.0.0` and later:

- **Major:** incompatible contract changes; reset Minor and Patch.
- **Minor:** compatible capabilities or public deprecations; reset Patch.
- **Patch:** compatible fixes; released documentation, packaging, and metadata corrections also use Patch when they preserve the contract.

Use the highest required bump in a release. During `0.x` development, compatible fixes increment Patch; features, deprecations, and incompatible changes increment Minor and reset Patch. Explain incompatibilities explicitly. Declare `1.0.0` when committing to a stable supported contract.

Prereleases use forms such as `1.2.0-alpha.1`, `1.2.0-beta.1`, or `1.2.0-rc.1`. Numeric prerelease identifiers have no leading zeroes; prereleases precede the corresponding stable version. Optional `+build.42` metadata does not affect ordering. Compare with SemVer precedence, not text or decimal-number ordering.

### Release workflow

Maintain one authoritative version per release unit. Derive mirrors where practical; otherwise update and verify them together with runtime displays, package metadata, lockfiles, installers, artifact names, and release notes as applicable. Keep ecosystem-specific prerelease encodings explicitly mapped to the product version. An OS-required four-part file version is packaging metadata, not a four-part product version.

Record the compatibility impact, migration/deprecation notes, checks performed, and limitations. Tag the exact validated source with the pattern below, using a new immutable tag. Published versions, tags, and assets are never overwritten to correct a release; publish a new forward version instead. A rollback release uses the same compatibility test.

Policy adoption and ordinary development commits do not automatically publish releases, build binaries, deploy services, or establish production readiness. A working tree may retain its previous version until release preparation; describe untagged changes as unreleased. Preserve historical release identities and data identifiers. New publication follows the active task authorization and existing branch protections.

### Project Release Checks

Verify source/UI/installer versions, existing library tests, and legacy-client update ordering; build and smoke-test the Windows artifacts in the supported environment.

## 中文

所有者决定：2026-10-10。本规则适用于本仓库后续发布。

### Release Unit and Contract

Media Manager 应用；媒体库及数据库格式、文件操作、配置、安装与更新行为。

### Version Source and Transition

权威版本来源：`src/version.py::__version__`。2026-10-10 核查到的源码值为 `0.0.4`。本次规则提交保留运行时版本，不发布新的应用版本。

历史发布包含 `v0.0.4.1`，而 main 当前报告 `0.0.4`。保留这两项事实及全部旧产物。该四段旧版本之后，首次兼容修复使用 `0.0.5`；新功能或不兼容变更使用 `0.1.0`，或按约定影响采用更高版本。不得将 `0.0.4.1` 重解释为构建元数据，也不得重新发布 `0.0.4`。交付前验证现有更新器对四段旧版本的升级顺序；当前更新器解析数字版本，尚未实现完整的 SemVer 预发布及构建元数据排序。在更新并验证该组件之前，自动更新仅使用稳定的纯数字版本。

发布标签格式：`vX.Y.Z`（例如 `v1.2.3`）。标签前缀不属于 SemVer 版本值。

### Version Rules

采用 [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html)：`MAJOR.MINOR.PATCH`，数字不含前导零。对于 `1.0.0` 及以上版本：

- **Major：** 不兼容的约定变更；Minor 与 Patch 归零。
- **Minor：** 兼容的新能力或公开弃用声明；Patch 归零。
- **Patch：** 兼容修复；发布不改变约定的文档、打包和元数据修正时也使用 Patch。

一次发布按最高影响等级递增。在 `0.x` 开发阶段，兼容修复递增 Patch；新功能、弃用和不兼容变更递增 Minor，并将 Patch 归零。不兼容变更必须明确说明。决定承诺稳定的受支持约定时采用 `1.0.0`。

预发布使用 `1.2.0-alpha.1`、`1.2.0-beta.1` 或 `1.2.0-rc.1` 等形式。预发布的纯数字标识不含前导零，排序低于对应稳定版。可选的 `+build.42` 构建元数据不影响排序。按 SemVer 优先级比较，不按字符串或小数比较。

### Release Workflow

每个发布单元只设一个权威版本来源。尽量自动派生镜像字段；需要手动同步时，将运行界面、包元数据、锁文件、安装程序、产物名称和发布说明中的相关版本一起更新并验证。生态系统专用的预发布编码必须明确映射到产品版本。操作系统要求的四段文件版本属于打包元数据，不是四段产品版本。

记录兼容性影响、迁移和弃用说明、实际检查及限制。使用下方约定为精确验证的源码提交建立新标签。已发布版本、标签和产物不得覆盖；修正须发布新的向前版本。回退发布也按兼容性影响选择版本。

采用规则及普通开发提交不会自动发布版本、构建二进制、部署服务或证明生产可用。准备发布前，工作树可以保留上一版本值，但未打标签的变更应明确称为尚未发布。保留历史发布身份和数据标识。新发布遵循当前任务授权与现有分支保护。

### Project Release Checks

核对源码、界面与安装包版本，运行现有媒体库测试并验证旧客户端升级顺序；在支持的环境构建和冒烟测试 Windows 产物。
