import graphene
from graphene_django import DjangoObjectType
from .models import User
from django.contrib.auth import get_user_model


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "first_name", "last_name", "bio", "avatar", "posts")


class RegisterUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        user = get_user_model()(
            email=email,
        )
        user.set_password(password)
        user.save()
        return RegisterUser(user=user)


class UpdateProfile(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        bio = graphene.String(required=False)
        avatar = graphene.String(required=False)

    def mutate(self, info, first_name=None, last_name=None, bio=None, avatar=None):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")

        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if bio is not None:
            user.bio = bio
        if avatar is not None:
            user.avatar = avatar

        user.save()
        return UpdateProfile(user=user)


class UserQuery(graphene.ObjectType):
    me = graphene.Field(UserType)

    def resolve_me(root, info):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        return user


class UserMutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    update_profile = UpdateProfile.Field()
