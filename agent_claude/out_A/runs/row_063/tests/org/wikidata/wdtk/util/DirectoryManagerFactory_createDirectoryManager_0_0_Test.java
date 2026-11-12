package org.wikidata.wdtk.util;

/*-
 * #%L
 * Wikidata Toolkit Utilities
 * %%
 * Copyright (C) 2014 - 2026 Wikidata Toolkit Developers
 * %%
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *      http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * #L%
 */

import static org.junit.Assert.*;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

import org.junit.After;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TemporaryFolder;

public class DirectoryManagerFactory_createDirectoryManager_0_0_Test {

	@Rule
	public TemporaryFolder tmp = new TemporaryFolder();

	private Class<? extends DirectoryManager> saved;

	public static class BaseDM implements DirectoryManager {
		public DirectoryManager getSubdirectoryManager(String s) { return null; }
		public boolean hasSubdirectory(String s) { return false; }
		public boolean hasFile(String s) { return false; }
		public long createFile(String f, InputStream in) { return 0; }
		public long createFileAtomic(String f, InputStream in) { return 0; }
		public void createFile(String f, String c) { }
		public OutputStream getOutputStreamForFile(String f) { return null; }
		public InputStream getInputStreamForFile(String f, CompressionType t) { return null; }
		public List<String> getSubdirectories(String g) { return null; }
	}

	public static class NoCtorDM extends BaseDM {
	}

	public static class RecordingDM extends BaseDM {
		public final Path path;
		public final Boolean readOnly;
		public RecordingDM(Path path, Boolean readOnly) {
			this.path = path;
			this.readOnly = readOnly;
		}
	}

	public static class IOExDM extends BaseDM {
		public IOExDM(Path path, Boolean readOnly) throws IOException {
			throw new IOException("io");
		}
	}

	public static class RtExDM extends BaseDM {
		public RtExDM(Path path, Boolean readOnly) {
			throw new IllegalStateException("rt");
		}
	}

	public static abstract class AbstractDM extends BaseDM {
		public AbstractDM(Path path, Boolean readOnly) {
		}
	}

	@Before
	public void setUp() {
		saved = DirectoryManagerFactory.dmClass;
	}

	@After
	public void tearDown() {
		DirectoryManagerFactory.setDirectoryManagerClass(saved);
	}

	@Test
	public void testDefaultImplReadOnly() throws IOException {
		DirectoryManagerFactory.setDirectoryManagerClass(DirectoryManagerImpl.class);
		String dir = tmp.getRoot().getAbsolutePath();
		DirectoryManager dm = DirectoryManagerFactory.createDirectoryManager(dir, true);
		assertTrue(dm instanceof DirectoryManagerImpl);
		assertTrue(((DirectoryManagerImpl) dm).readOnly);
		assertEquals(Paths.get(dir), ((DirectoryManagerImpl) dm).directory);
	}

	@Test
	public void testDefaultImplWritableCreatesDirectory() throws IOException {
		DirectoryManagerFactory.setDirectoryManagerClass(DirectoryManagerImpl.class);
		File sub = new File(tmp.getRoot(), "newdir");
		DirectoryManager dm = DirectoryManagerFactory.createDirectoryManager(sub.getAbsolutePath(), false);
		assertFalse(((DirectoryManagerImpl) dm).readOnly);
		assertTrue(sub.isDirectory());
	}

	@Test(expected = IOException.class)
	public void testDefaultImplReadOnlyNonExisting() throws IOException {
		DirectoryManagerFactory.setDirectoryManagerClass(DirectoryManagerImpl.class);
		DirectoryManagerFactory.createDirectoryManager(
				new File(tmp.getRoot(), "nonexisting/123").getAbsolutePath(), true);
	}

	@Test
	public void testCustomClassReceivesArgs() throws IOException {
		DirectoryManagerFactory.setDirectoryManagerClass(RecordingDM.class);
		DirectoryManager dm = DirectoryManagerFactory.createDirectoryManager("some/dir", false);
		assertTrue(dm instanceof RecordingDM);
		assertEquals(Paths.get("some/dir"), ((RecordingDM) dm).path);
		assertEquals(Boolean.FALSE, ((RecordingDM) dm).readOnly);
	}

	@Test
	public void testNoConstructor() throws IOException {
		DirectoryManagerFactory.setDirectoryManagerClass(NoCtorDM.class);
		try {
			DirectoryManagerFactory.createDirectoryManager("/", true);
			fail();
		} catch (RuntimeException e) {
			assertTrue(e.getCause() instanceof NoSuchMethodException);
		}
	}

	@Test
	public void testAbstractClass() throws IOException {
		DirectoryManagerFactory.setDirectoryManagerClass(AbstractDM.class);
		try {
			DirectoryManagerFactory.createDirectoryManager("/", true);
			fail();
		} catch (RuntimeException e) {
			assertTrue(e.getCause() instanceof InstantiationException);
		}
	}

	@Test
	public void testConstructorThrowsIOException() {
		DirectoryManagerFactory.setDirectoryManagerClass(IOExDM.class);
		try {
			DirectoryManagerFactory.createDirectoryManager("x", true);
			fail();
		} catch (IOException e) {
			assertEquals("io", e.getMessage());
		}
	}

	@Test
	public void testConstructorThrowsRuntimeException() throws IOException {
		DirectoryManagerFactory.setDirectoryManagerClass(RtExDM.class);
		try {
			DirectoryManagerFactory.createDirectoryManager("x", true);
			fail();
		} catch (RuntimeException e) {
			assertTrue(e.getCause() instanceof IllegalStateException);
			assertEquals("rt", e.getCause().getMessage());
		}
	}

	@Test(expected = NullPointerException.class)
	public void testNullDirectory() throws IOException {
		DirectoryManagerFactory.createDirectoryManager((String) null, true);
	}
}
