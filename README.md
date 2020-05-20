# github-oauth-gateway

Gateway for authenticating with GitHub using OAuth.

Primarily used by
[Assemblé](https://github.com/HDI-Project/ballet-assemble)
to authenticate Jupyter Lab sessions with GitHub.

There is a free and public deployment at https://github-oauth-gateway.herokuapp.com or you
can deploy your own instance.

## Usage

1. get this gateway app's client ID
2. initiate the OAuth login flow with GitHub, providing the client ID from
   step 1 as well as a secret key of your choice. After successful
   authorization, GitHub will send a secret code to the gateway.
3. request an access token from the gateway; it will exchange the secret code
   for an access token with GitHub, send you the access token, and delete any
   record of your request.
   
## Deployment

There is a reference deployment at https://github-oauth-gateway.herokuapp.com/

### API Reference

#### app_id

Get the GitHub OAuth App ID of the github-oauth-gateway app
```
GET /api/v1/app_id
```

Example response
```json
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
```json
{"access_token":"e72e16c7e42f292c6912e7710c838347ae178b4a", "scope":"repo,gist", "token_type":"bearer", "message":  null}
```
