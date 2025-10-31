from rest_framework import serializers
from . import models


class BlogSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BlogSection
        fields = ("id", "order", "section_type", "content")


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = ("id", "title", "slug", "summary", "status", "published_at", "reading_time_minutes", "cover_image")


class BlogDetailSerializer(BlogSerializer):
    sections = BlogSectionSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta(BlogSerializer.Meta):
        fields = BlogSerializer.Meta.fields + ("sections", "comments_count", "likes_count", "comments")

    def get_comments(self, obj):
        qs = obj.comments.filter(is_public=True).select_related("author")
        return build_comment_tree(qs)


class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BlogComment
        fields = ("id", "blog", "parent", "author", "author_name", "body", "is_public", "created_at")
        read_only_fields = ("author", "created_at")

    def validate(self, data):
        parent = data.get("parent")
        if parent:
            # enforce max depth 3
            depth = 0
            p = parent
            while p:
                depth += 1
                p = p.parent
                if depth >= 3:
                    raise serializers.ValidationError("Maximum comment nesting depth (3) exceeded")
        return data


def build_comment_tree(comments_qs):
    # build a nested comment tree up to depth 3
    nodes = {}
    roots = []
    for c in comments_qs.order_by("created_at"):
        nodes[c.id] = {"id": c.id, "blog": c.blog_id, "parent": c.parent_id, "author": c.author_id, "author_name": c.author_name, "body": c.body, "is_public": c.is_public, "created_at": c.created_at, "replies": []}
    for nid, node in nodes.items():
        parent = node["parent"]
        if parent and parent in nodes:
            # attach as child if depth < 3
            # compute depth by walking parents up to root (cheap for small trees)
            depth = 0
            p = parent
            while p and p in nodes and depth < 4:
                depth += 1
                p = nodes[p]["parent"]
            if depth <= 3:
                nodes[parent]["replies"].append(node)
            else:
                roots.append(node)
        else:
            roots.append(node)
    return roots


class BlogLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BlogLike
        fields = ("id", "blog", "user", "created_at")
        read_only_fields = ("created_at",)


class LeadFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeadForm
        fields = ("id", "name", "slug", "form_unique_id", "form_page_url", "description", "schema", "form_settings", "active")


class FormSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FormSubmission
        fields = ("id", "form", "payload", "submitter_ip", "user_agent", "status", "lead_ref", "forwarded_at", "forwarded_response", "created_at")
        read_only_fields = ("status", "lead_ref", "forwarded_at", "forwarded_response", "created_at")

    def validate(self, data):
        # Basic validation: if form has schema, and jsonschema is available, validate payload
        form = data.get("form")
        payload = data.get("payload")
        schema = getattr(form, "schema", None)
        if schema:
            try:
                import jsonschema

                jsonschema.validate(instance=payload, schema=schema)
            except ImportError:
                # jsonschema not installed — skip strict validation
                pass
            except jsonschema.ValidationError as exc:
                raise serializers.ValidationError({"payload": str(exc)})
        return data
