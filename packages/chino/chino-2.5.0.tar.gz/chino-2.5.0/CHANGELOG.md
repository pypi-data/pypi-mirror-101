# Changelog

## [2.5.0] 2021-04-09
- Added support for datatype conversion and dump schema

## [2.4.0] 2021-03-18
- Deprecated old Search API in favor of the new one. Added ad hoc methods to
  search over docs and users
- Deprecated old Consent Management API in favor of the new 
  [Consenta API](https://docs.chino.io/consent/consentame/docs/v1).

## [2.3.0] 2020-10-26 
- Added support for the 'default' attribute in Schema and UserSchema fields
  definition

## [2.2.0] 2020-09-24 
- Added url/token for blob

## [2.1.0] 2020-09-04
- Added support for Documents PATCH (partial update)
- Repositories LIST: added support for search filter 'descr' (URL query param)
- Schemas LIST: added support for search filter 'descr' (URL query param)
- UserSchemas LIST: added support for search filter 'descr' (URL query param)
- Groups LIST: added support for search filter 'name' (URL query param)
- Collections LIST: added support for filtering by 'document_id' (list only the
  collections which keeps that document)
