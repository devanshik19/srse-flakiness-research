package nonapi.io.github.classgraph.fastzipfilereader;

import nonapi.io.github.classgraph.fastzipfilereader.FastZipEntry;
import nonapi.io.github.classgraph.fastzipfilereader.LogicalZipFile;
import nonapi.io.github.classgraph.fastzipfilereader.NestedJarHandler;
import nonapi.io.github.classgraph.utils.FileUtils;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.attribute.PosixFilePermission;
import java.util.Collections;
import java.util.Set;
import static org.mockito.ArgumentMatchers.anyLong;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.io.EOFException;
import java.nio.Buffer;
import java.nio.BufferUnderflowException;
import java.nio.ByteBuffer;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.zip.DataFormatException;
import java.util.zip.Inflater;
import java.util.zip.ZipException;
import nonapi.io.github.classgraph.recycler.RecycleOnClose;
import nonapi.io.github.classgraph.utils.VersionFinder;

class FastZipEntry_load_4_0_Test {

    private FastZipEntry fastZipEntry;

    private LogicalZipFile mockLogicalZipFile;

    private NestedJarHandler mockNestedJarHandler;

    @BeforeEach
    void setUp() {
        mockLogicalZipFile = mock(LogicalZipFile.class);
        mockNestedJarHandler = mock(NestedJarHandler.class);
        Set<PosixFilePermission> permissions = Collections.emptySet();
        fastZipEntry = new FastZipEntry(mockLogicalZipFile, 0L, "testEntry", false, 100L, 100L, mockNestedJarHandler, 0L, permissions);
    }

    @Test
    void testLoad() throws IOException, InterruptedException {
        InputStream mockInputStream = mock(InputStream.class);
        when(mockInputStream.read(any(byte[].class), anyInt(), anyInt())).thenReturn(-1);
        when(mockInputStream.read()).thenReturn(-1);
        FastZipEntry spyEntry = Mockito.spy(fastZipEntry);
        doReturn(mockInputStream).when(spyEntry).open();
        byte[] expectedBytes = new byte[0];
        byte[] actualBytes = spyEntry.load();
        assertArrayEquals(expectedBytes, actualBytes);
        verify(mockInputStream, times(1)).close();
    }

    @Test
    void testLoadIOException() throws IOException, InterruptedException {
        FastZipEntry spyEntry = Mockito.spy(fastZipEntry);
        doThrow(new IOException("Test Exception")).when(spyEntry).open();
        assertThrows(IOException.class, spyEntry::load);
    }
}
