import graphene
from graphene_django import DjangoObjectType
from .models import Comment, Post, Reaction


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = (
            "id",
            "content_text",
            "author",
            "created_at",
            "updated_at",
            "comments",
            "reactions",
        )


class Reactiontype(DjangoObjectType):
    class Meta:
        model = Reaction
        fields = ("id", "states", "user", "post")


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "content_text", "user", "post", "created_at", "updated_at")


class CreateReaction(graphene.Mutation):
    reaction = graphene.Field(Reactiontype)

    class Arguments:
        states = graphene.String(required=True)
        post = graphene.ID(required=True)

    def mutate(self, info, states, post):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        post_instance = Post.objects.get(pk=post)
        reaction = Reaction.objects.create(post=post_instance, states=states, user=user)
        return CreateReaction(reaction)


class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        content_text = graphene.String(required=True)
        post = graphene.ID(required=True)

    def mutate(self, info, content_text, post):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        post_instance = Post.objects.get(pk=post)
        comment = Comment.objects.create(
            post=post_instance, content_text=content_text, user=user
        )
        return CreateComment(comment)


class CreatePost(graphene.Mutation):
    class Arguments:
        content = graphene.String(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, content):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        post = Post.objects.create(author=user, content_text=content)
        return CreatePost(post=post)


class PostQuery(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    posts_by_user = graphene.List(PostType, user_id=graphene.ID(required=True))

    def resolve_all_posts(root, info):
        return Post.objects.select_related("author").all()

    def resolve_posts_by_user(root, info, user_id):
        return Post.objects.filter(author_id=user_id)


class PostMutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    create_comment = CreateComment.Field()
    create_reaction = CreateReaction.Field()
