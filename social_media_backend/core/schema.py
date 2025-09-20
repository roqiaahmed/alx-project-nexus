import graphene
from users.schema import UserQuery, UserMutation
from posts.schema import PostQuery, PostMutation
import graphene
import graphql_jwt


class Query(UserQuery, PostQuery, graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")


class Mutation(UserMutation, PostMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
