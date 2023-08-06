# README #

Esta lib é um atualizador para os servidores.

A lib tem como base um comando manage.py chamado update_server, que recebe os seguintes parâmetros:
**'project_name', 'host', 'user', 'server_password', 'git_user_password','has_websockets','has_cronjobs'**, sendo os
dois últimos False por padrão.

`py manage.py update_server textil 138.197.67.44 root senha senha_do_git`

A URL **/webhooks/push_request** pode ser configurada no Bitbucket para cada push realizado, assim, a atualização do
servidor será feita de forma automática, pois o webhook chama a atualização do servidor, juntamente com um backup do
banco de dados pré-atualização. Essa rotina evita que cada servidor local que possuímos necessite de uma conexão por
TeamViewer, economizando tempo dos desenvolvedores e também dos clientes

# Configurações

No arquivo de configurações do projeto (settings.py), é necessário incluir as variaveis

`
SERVER_BRANCH = nome da branch que será usada (Ex:server)
`

`SERVER_SETTINGS = { HOST:HOST:, USER:USER:, PASSWORD:PASSWORD:, GIT_PASSWORD:GIT_PASSWORD:, GIT_USER:GIT_USER:, HAS_WEBSOCKETS:HAS_WEBSOCKETS, HAS_CRONJOBS:HAS_CRONJOBS}
`
assim como **singular_server_updater** no installed_apps
No arquivo de urls, inclua a url do webhook no urlpatterns:
`urlspatterns=[*routes.urlpatterns.....................
`