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


class UpdateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        id = graphene.ID(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, id, content):
        user = info.context.user
        comment = Comment.objects.get(id=id)

        if comment.user != user:
            raise Exception("You cannot update someone else’s comment")

        comment.content_text = content
        comment.save()
        return UpdateComment(comment=comment)


class DeleteComment(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        user = info.context.user
        comment = Comment.objects.get(id=id)

        if comment.user != user:
            raise Exception("You cannot delete someone else’s comment")

        comment.delete()
        return DeleteComment(ok=True)


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


class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        id = graphene.ID(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, id, content):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")

        post = Post.objects.get(id=id)

        if post.author != user:
            raise Exception("You cannot update someone else’s post")

        if content == "":
            raise Exception("content must not be empyt")
        post.content_text = content
        post.save()
        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        user = info.context.user
        post = Post.objects.get(id=id)

        if post.author != user:
            raise Exception("You cannot delete someone else’s post")

        post.delete()
        return DeletePost(ok=True)


class PostQuery(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    posts_by_user = graphene.List(PostType, user_id=graphene.ID(required=True))

    def resolve_all_posts(root, info):
        return Post.objects.select_related("author").all()

    def resolve_posts_by_user(root, info, user_id):
        return Post.objects.filter(author_id=user_id)


class PostMutation(graphene.ObjectType):
    # Create
    create_post = CreatePost.Field()
    create_comment = CreateComment.Field()
    create_reaction = CreateReaction.Field()

    # Update
    update_post = UpdatePost.Field()
    update_comment = UpdateComment.Field()

    # Delete
    delete_post = DeletePost.Field()
    delete_comment = DeleteComment.Field()
