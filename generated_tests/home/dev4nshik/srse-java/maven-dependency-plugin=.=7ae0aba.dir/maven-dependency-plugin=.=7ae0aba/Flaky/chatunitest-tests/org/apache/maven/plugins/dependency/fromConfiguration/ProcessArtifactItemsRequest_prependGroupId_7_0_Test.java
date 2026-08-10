package org.apache.maven.plugins.dependency.fromConfiguration;

import java.lang.reflect.Method;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

public class ProcessArtifactItemsRequest_prependGroupId_7_0_Test {

    @Test
    public void testPrependGroupId() throws Exception {
        // Create an instance of the class using the no-argument constructor
        ProcessArtifactItemsRequest request = new ProcessArtifactItemsRequest();
        // Use reflection to access the private field 'prependGroupId'
        Method setPrependGroupIdMethod = ProcessArtifactItemsRequest.class.getDeclaredMethod("setPrependGroupId", boolean.class);
        Method isPrependGroupIdMethod = ProcessArtifactItemsRequest.class.getDeclaredMethod("isPrependGroupId");
        setPrependGroupIdMethod.setAccessible(true);
        isPrependGroupIdMethod.setAccessible(true);
        // Test the prependGroupId method with true
        request.prependGroupId(true);
        assertTrue((Boolean) isPrependGroupIdMethod.invoke(request), "prependGroupId should be true");
        // Test the prependGroupId method with false
        request.prependGroupId(false);
        assertFalse((Boolean) isPrependGroupIdMethod.invoke(request), "prependGroupId should be false");
    }
}
