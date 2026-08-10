package org.apache.maven.plugins.dependency.fromConfiguration;

import java.lang.reflect.Method;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

public class ProcessArtifactItemsRequest_removeVersion_4_0_Test {

    @Test
    public void testRemoveVersion() throws Exception {
        // Create an instance of the class
        ProcessArtifactItemsRequest request = new ProcessArtifactItemsRequest();
        // Use reflection to access the private field 'removeVersion'
        Method isRemoveVersionMethod = ProcessArtifactItemsRequest.class.getDeclaredMethod("isRemoveVersion");
        isRemoveVersionMethod.setAccessible(true);
        // Test when removeVersion is set to true
        request.removeVersion(true);
        assertTrue((boolean) isRemoveVersionMethod.invoke(request), "removeVersion should be true");
        // Test when removeVersion is set to false
        request.removeVersion(false);
        assertFalse((boolean) isRemoveVersionMethod.invoke(request), "removeVersion should be false");
    }
}
