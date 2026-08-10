package com.intel.jndn.utils.client.impl;

import com.intel.jndn.utils.client.DataStream;
import net.named_data.jndn.Data;
import net.named_data.jndn.Face;
import net.named_data.jndn.Interest;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.io.IOException;
import java.util.logging.Logger;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import com.intel.jndn.utils.client.SegmentedClient;
import com.intel.jndn.utils.impl.SegmentationHelper;
import net.named_data.jndn.Name;
import net.named_data.jndn.Name.Component;
import net.named_data.jndn.OnData;

@ExtendWith(MockitoExtension.class)
class DefaultSegmentedClient_getSegmentsAsync_1_1_Test {

    @Mock
    private Face mockFace;

    @Mock
    private Interest mockInterest;

    @Test
    void testGetSegmentsAsync() throws IOException {
        // Arrange
        DefaultSegmentedClient segmentedClient = DefaultSegmentedClient.getDefault();
        DefaultSegmentedClient spyClient = spy(segmentedClient);
        SegmentedDataStream stream = new SegmentedDataStream();
        doReturn(stream).when(spyClient).getSegmentsAsync(any(), any());
        // Act
        DataStream result = spyClient.getSegmentsAsync(mockFace, mockInterest);
        // Assert
        assertNotNull(result);
        verify(mockFace).expressInterest(eq(mockInterest), eq(stream), eq(stream));
    }
}
