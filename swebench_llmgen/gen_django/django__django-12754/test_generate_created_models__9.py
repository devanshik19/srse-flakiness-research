import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations import autodetector, operations
from django.db.migrations.state import ProjectState

class TestMigrationAutodetector:
    def setup_method(self):
        self.old_state = ProjectState()
        self.new_state = ProjectState()
        self.questioner = None  # You can mock this if necessary

        self.detector = autodetector.MigrationAutodetector(self.old_state, self.new_state, self.questioner)

    def test_generate_created_models(self):
        # Prepare old and new states
        self.old_state.add_model("auth", "User", {
            "id": models.AutoField(primary_key=True),
            "username": models.CharField(max_length=150, unique=True),
        })

        self.new_state.add_model("auth", "User", {
            "id": models.AutoField(primary_key=True),
            "username": models.CharField(max_length=150, unique=True),
            "email": models.EmailField(),
            "first_name": models.CharField(max_length=30, blank=True),
            "last_name": models.CharField(max_length=30, blank=True),
        })

        self.detector.old_model_keys = {("auth", "User")}
        self.detector.new_model_keys = {("auth", "User")}
        self.detector.to_state = self.new_state
        
        # Add attributes to use in the method
        self.detector.new_apps = self.new_state

        self.detector.generate_created_models()

        operations_list = self.detector.operations["auth"]
        assert len(operations_list) == 1
        assert isinstance(operations_list[0], operations.CreateModel)
        assert operations_list[0].name == "User"
        assert "email" in dict(operations_list[0].fields)
        assert "first_name" in dict(operations_list[0].fields)
        assert "last_name" in dict(operations_list[0].fields)

        # Check operations for fields
        self.detector.old_model_keys = set()
        self.detector.new_model_keys = {("auth", "User")}
        self.detector.to_state = self.new_state
        self.detector.generate_created_models()

        assert len(self.detector.operations["auth"]) == 1  # Operation only generated once for create
        
        # Check managed models
        self.detector.new_state.models["auth", "User"]._meta.managed = False
        self.detector.generate_created_models()
        assert len(self.detector.operations["auth"]) == 1  # Unmanaged model should not add operations