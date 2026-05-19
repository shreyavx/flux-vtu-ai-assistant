from django.contrib import admin

from .models import (
    Project,
    Document,
    DocumentChunk
)

admin.site.register(Project)
admin.site.register(Document)
@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'document',
        'embedding_id',
        'short_chunk'
    )

    def short_chunk(self, obj):

        return obj.chunk_text[:50]