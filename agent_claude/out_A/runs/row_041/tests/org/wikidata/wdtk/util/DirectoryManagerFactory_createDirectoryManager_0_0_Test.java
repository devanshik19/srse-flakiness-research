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

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class DirectoryManagerFactory_createDirectoryManager_0_0_Test {

	public static class IoFailingDM extends DirectoryManagerImpl {
		public IoFailingDM(Path p, Boolean r) throws IOException {
			super(p, r);
			throw new IOException("io-fail");
		}
	}

	public static class RuntimeFailingDM extends DirectoryManagerImpl {
		public RuntimeFailingDM(Path p, Boolean r) throws IOException {
			super(p, r);
			throw new IllegalStateException("rt-fail");
		}
	}

	public static abstract class AbstractDM extends DirectoryManagerImpl {
		public AbstractDM(Path p, Boolean r) throws IOException {
			super(p, r);
		}
	}

	public static class NoCtorDM extends DirectoryManagerImpl {
		public NoCtorDM(String s) throws IOException {
			super(Paths.get(s), true);
		}
	}

	private Path cwd;

	@Before
	public void setUp() {
		cwd = Paths.get(System.getProperty("user.dir"));
		DirectoryManagerFactory.setDirectoryManagerClass(DirectoryManagerImpl.class);
	}

	@After
	public void tearDown() {
		DirectoryManagerFactory.setDirectoryManagerClass(DirectoryManagerImpl.class);
	}

	@Test
	public void testSuccessReadOnly() throws IOException {
		DirectoryManager dm = DirectoryManagerFactory.createDirectoryManager(cwd, true);
		assertTrue(dm instanceof DirectoryManagerImpl);
		assertTrue(((DirectoryManagerImpl) dm).readOnly);
		assertEquals(cwd, ((DirectoryManagerImpl) dm).directory);
	}

	@Test
	public void testSuccessWritable() throws IOException {
		DirectoryManager dm = DirectoryManagerFactory.createDirectoryManager(cwd, false);
		assertFalse(((DirectoryManagerImpl) dm).readOnly);
	}

	@Test
	public void testIOExceptionFromImpl() {
		try {
			DirectoryManagerFactory.createDirectoryManager(
					Paths.get("/nonexisting-directory/123456789/hopefully"), true);
			fail();
		} catch (IOException e) {
			// expected
		}
	}

	@Test
	public void testIOExceptionFromCustom() {
		DirectoryManagerFactory.setDirectoryManagerClass(IoFailingDM.class);
		try {
			DirectoryManagerFactory.createDirectoryManager(cwd, true);
			fail();
		} catch (IOException e) {
			assertEquals("io-fail", e.getMessage());
		}
	}

	@Test
	public void testRuntimeExceptionFromConstructor() throws IOException {
		DirectoryManagerFactory.setDirectoryManagerClass(RuntimeFailingDM.class);
		try {
			DirectoryManagerFactory.createDirectoryManager(cwd, true);
			fail();
		} catch (RuntimeException e) {
			assertTrue(e.getCause() instanceof IllegalStateException);
			assertEquals("rt-fail", e.getCause().getMessage());
		}
	}

	@Test
	public void testInstantiationException() throws IOException {
		DirectoryManagerFactory.setDirectoryManagerClass(AbstractDM.class);
		try {
			DirectoryManagerFactory.createDirectoryManager(cwd, true);
			fail();
		} catch (RuntimeException e) {
			assertTrue(e.getCause() instanceof InstantiationException);
		}
	}

	@Test
	public void testNoSuchMethod() throws IOException {
		DirectoryManagerFactory.setDirectoryManagerClass(NoCtorDM.class);
		try {
			DirectoryManagerFactory.createDirectoryManager(cwd, true);
			fail();
		} catch (RuntimeException e) {
			assertTrue(e.getCause() instanceof NoSuchMethodException);
		}
	}

	@Test
	public void testNoConstructorInterfaceImpl() throws IOException {
		DirectoryManagerFactory.setDirectoryManagerClass(
				DirectoryManagerFactoryTest.TestDirectoryManager.class);
		try {
			DirectoryManagerFactory.createDirectoryManager(cwd, true);
			fail();
		} catch (RuntimeException e) {
			assertTrue(e.getCause() instanceof NoSuchMethodException);
		}
	}
}
