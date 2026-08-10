package org.apache.maven.plugins.dependency.fromConfiguration;

import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

public class ProcessArtifactItemsRequest_useBaseVersion_10_0_Test {

    @Test
    public void testUseBaseVersion_true() throws Exception {
        ProcessArtifactItemsRequest request = new ProcessArtifactItemsRequest();
        // Use reflection to access the private field
        java.lang.reflect.Field useBaseVersionField = ProcessArtifactItemsRequest.class.getDeclaredField("useBaseVersion");
        useBaseVersionField.setAccessible(true);
        // Call the method with true
        request.useBaseVersion(true);
        // Assert that the field was set correctly
        assertTrue((boolean) useBaseVersionField.get(request));
    }

    @Test
    public void testUseBaseVersion_false() throws Exception {
        ProcessArtifactItemsRequest request = new ProcessArtifactItemsRequest();
        // Use reflection to access the private field
        java.lang.reflect.Field useBaseVersionField = ProcessArtifactItemsRequest.class.getDeclaredField("useBaseVersion");
        useBaseVersionField.setAccessible(true);
        // Call the method with false
        request.useBaseVersion(false);
        // Assert that the field was set correctly
        assertFalse((boolean) useBaseVersionField.get(request));
    }
}
