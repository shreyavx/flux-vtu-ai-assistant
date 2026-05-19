from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    title = models.CharField(max_length=255)

    file = models.FileField(upload_to='documents/')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class DocumentChunk(models.Model):
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='chunks'
    )

    chunk_text = models.TextField()

    embedding_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chunk from {self.document.title}"