# github-oauth-gateway

Gateway for authenticating with GitHub using OAuth.

Mainly used by [ballet-submit-labextension](https://github.com/HDI-Project
/ballet-submit-labextension) to authenticate Jupyter notebook sessions with
GitHub.

## Usage

### API Reference

#### app_id

Get the GitHub OAuth App ID of the github-oauth-gateway app
```
GET /api/v1/app_id
```

Example response
```
{"client_id":"5fdfc609dd0081352b93","message":null}
```

#### access_token

Exchange the secret state for an OAuth access token

```
POST /api/v1/access_token
```

| param | value |
|-------|-------|
| state | secret state (required) |

Example response



