# Examples of AI-generated flaky tests

Details of the 8 flaky tests found across all experiments —> 2 non-deterministic (ND), 6 order-dependent (OD)

## 1. marine-api Time#toString (ND, passes 17 / 100)

* Generator: ChatUniTest (gpt-4o)
* Project: [ktuukkan/marine-api](https://github.com/ktuukkan/marine-api) @ 0a1f308
* Focal method: net.sf.marineapi.nmea.util.Time#toString
* Mechanism: the no-arg constructor new Time() reads the system clock; the test rebuilds the expected string with %05.3f, which does not zero-pad the whole-number part. When the clock-seconds are a single digit (10 of every 60 seconds ≈ 17%), it expects "3.000" while toString() returns "03.000" and the assertion fails.

GENERATED TEST:

```java
@BeforeEach
public void setUp() {
    time = new Time();
}

@Test
public void testToStringDefaultConstructor() {
    try {
        Method getHourMethod = Time.class.getDeclaredMethod("getHour");
        Method getMinutesMethod = Time.class.getDeclaredMethod("getMinutes");
        Method getSecondsMethod = Time.class.getDeclaredMethod("getSeconds");
        getHourMethod.setAccessible(true);
        getMinutesMethod.setAccessible(true);
        getSecondsMethod.setAccessible(true);
        int hour = (int) getHourMethod.invoke(time);
        int minutes = (int) getMinutesMethod.invoke(time);
        double seconds = (double) getSecondsMethod.invoke(time);
        String expected = String.format("%02d%02d%05.3f", hour, minutes, seconds);
        assertEquals(expected, time.toString());
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```

DEVELOPER'S TEST for the same method (not flaky):

```java
@Test
public void testFormatTimeWithDecimals() {
    Time t = new Time(1, 2, 3.456);
    assertEquals("010203.456", t.toString());
}

@Test
public void testFormatTimeWithOneDecimal() {
    Time t = new Time(1, 2, 3.4);
    assertEquals("010203.400", t.toString());
}
```

## 2. mercury getJournaledRoutes (ND)

* Generator: ChatUniTest (gpt-4o), focal-targeted · Kind: non-deterministic (shared-state / order-dependent, surfaced through plain reruns)
* Project: [Accenture/mercury](https://github.com/Accenture/mercury) @ e659caf000c2a714d921a52cbc85e13f56cef981, module system/platform-core
* Focal method: PostOffice#getJournaledRoutes (system/platform-core/src/main/java/org/platformlambda/core/system/PostOffice.java). This was the disagreement case: the LLM picked getJournaledRoutes (the real method under test), Jaccard picked getInstance (the singleton accessor). The LLM was right.
* Mechanism: journaledRoutes is a shared static map on the EventEmitter singleton with no per-test cleanup, so it accumulates across test methods and within the JVM. The generated test asserts on its .size() assuming known state:

  * testGetJournaledRoutes_Empty asserts size == 0. Passes when the map is empty, fails with expected <0> but was <2> when a prior method or run already populated it.
  * testGetJournaledRoutes_NonEmpty adds 2 and asserts size == 2. Fails with expected <2> but was <4> when the 2 it adds stack on the 2 already present.
* Rate: FLAKY, fails intermittently (1 to 2 failing methods across reruns), because JUnit does not guarantee method order and the static map persists.
* Confirmation: the ND rerun is conclusive; NonDex/iDFlakies would likely also flag it since it is shared-state driven.

GENERATED TEST: (could not retrieve)

DEVELOPER'S TEST for the same method (not flaky):

```java
@Test
public void journalYamlTest() {
    String MY_FUNCTION = "my.test.function";
    String ANOTHER_FUNCTION = "another.function";
    EventEmitter po = EventEmitter.getInstance();
    List<String> routes = po.getJournaledRoutes();   // asserts the exact 2 routes configured in journal.yaml
    Assert.assertEquals(2, routes.size());
    Assert.assertEquals(ANOTHER_FUNCTION, routes.get(0));
    Assert.assertEquals(MY_FUNCTION, routes.get(1));
}
```

The developer works with the shared state (asserts the known 2 configured routes); the AI test assumed it controlled the map (empty, or exactly its own 2) and flaked when the pre-existing entries were present.

## 3-6. ormlite-core (×4) (OD)

* Generator: ChatUniTest (gpt-4o), focal-targeted
* Project: [j256/ormlite-core](https://github.com/j256/ormlite-core) @ 632b87c2a455b8eab4a6c09324e1f166273588d8
* Focal methods (impl RuntimeExceptionDao, interface Dao):

  * createIfNotExists
  * createObjectInstance
  * queryRaw
  * endThreadConnection
* Mechanism: each generated test passes 100/100 alone and is clean under NonDex, but flips inside the full developer suite.

  * A polluter earlier in the run leaves shared DAO/connection state and the generated test makes no attempt to isolate itself from it. Reproduced with independently regenerated bodies.
* Developer source tests: RuntimeExceptionDaoTest#{testCreateIfNotExistsThrow, testCreateObjectInstanceThrows, testQueryRawRowMapperThrow, testEndThreadConnectionThrows}.

GENERATED TEST (createIfNotExists):

```java
public class RuntimeExceptionDao_createIfNotExists_19_0_Test {

    // stubbed Dao: passes alone, order-dependent only in the full suite
    private RuntimeExceptionDao<TestEntity, Integer> runtimeExceptionDao;
    private Dao<TestEntity, Integer> mockDao;
    private Supplier<TestEntity> entitySupplier;
    private TestEntity testEntity;

    @BeforeEach
    public void setUp() {
        mockDao = mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
        entitySupplier = () -> new TestEntity(1, "Test");
        testEntity = new TestEntity(1, "Test");
    }

    @Test
    public void testCreateIfNotExistsSuccess() throws SQLException {
        when(mockDao.createIfNotExists(1, entitySupplier)).thenReturn(testEntity);
        TestEntity result = runtimeExceptionDao.createIfNotExists(1, entitySupplier);
        assertNotNull(result);
        assertEquals(testEntity, result);
        verify(mockDao, times(1)).createIfNotExists(1, entitySupplier);
    }

    @Test
    public void testCreateIfNotExistsThrowsSQLException() throws SQLException {
        when(mockDao.createIfNotExists(1, entitySupplier)).thenThrow(new SQLException("Error"));
        Exception exception = assertThrows(RuntimeException.class,
            () -> runtimeExceptionDao.createIfNotExists(1, entitySupplier));
        assertTrue(exception.getCause() instanceof SQLException);
        assertEquals("Error", exception.getCause().getMessage());
        verify(mockDao, times(1)).createIfNotExists(1, entitySupplier);
    }

    private static class TestEntity {
        private int id;
        private String name;
        public TestEntity(int id, String name) { this.id = id; this.name = name; }
        @Override public boolean equals(Object obj) {
            if (this == obj) return true;
            if (obj == null || getClass() != obj.getClass()) return false;
            TestEntity that = (TestEntity) obj;
            return id == that.id && name.equals(that.name);
        }
        @Override public int hashCode() { return Objects.hash(id, name); }
    }
}
```

GENERATED TEST (createObjectInstance):

```java
public class RuntimeExceptionDao_createObjectInstance_95_0_Test {

    // stubbed Dao: passes alone, order-dependent only in the full suite
    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;
    private Dao<Object, Object> mockDao;

    @BeforeEach
    public void setUp() {
        mockDao = mock(Dao.class);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testCreateObjectInstanceSuccess() throws SQLException {
        Object expectedObject = new Object();
        when(mockDao.createObjectInstance()).thenReturn(expectedObject);
        assertEquals(expectedObject, runtimeExceptionDao.createObjectInstance());
        verify(mockDao, times(1)).createObjectInstance();
    }

    @Test
    public void testCreateObjectInstanceThrowsSQLException() throws SQLException {
        when(mockDao.createObjectInstance()).thenThrow(new SQLException("Test exception"));
        Exception exception = assertThrows(RuntimeException.class,
            () -> runtimeExceptionDao.createObjectInstance());
        assertTrue(exception.getCause() instanceof SQLException);
        assertEquals("Test exception", exception.getCause().getMessage());
        verify(mockDao, times(1)).createObjectInstance();
    }
}
```

GENERATED TEST (queryRaw):

```java
public class RuntimeExceptionDao_queryRaw_40_0_Test {

    // stubbed Dao: passes alone, order-dependent only in the full suite
    @Mock private Dao<Object, Object> mockDao;
    @Mock private GenericRawResults<String[]> mockResults;
    private RuntimeExceptionDao<Object, Object> runtimeExceptionDao;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        runtimeExceptionDao = new RuntimeExceptionDao<>(mockDao);
    }

    @Test
    public void testQueryRawSuccess() throws SQLException {
        String query = "SELECT * FROM table";
        String[] arguments = { "arg1", "arg2" };
        when(mockDao.queryRaw(query, arguments)).thenReturn(mockResults);
        assertEquals(mockResults, runtimeExceptionDao.queryRaw(query, arguments));
        verify(mockDao, times(1)).queryRaw(query, arguments);
    }

    @Test
    public void testQueryRawThrowsSQLException() throws Exception {
        String query = "SELECT * FROM table";
        String[] arguments = { "arg1", "arg2" };
        when(mockDao.queryRaw(query, arguments)).thenThrow(new SQLException("SQL Exception"));
        RuntimeException exception = assertThrows(RuntimeException.class,
            () -> runtimeExceptionDao.queryRaw(query, arguments));
        assertEquals("SQL Exception", exception.getCause().getMessage());
        verify(mockDao, times(1)).queryRaw(query, arguments);
    }
}
```

GENERATED TEST (endThreadConnection): [could not retrieve].

## 7. sympy-24213 (OD polluter)

* Generator: SWT-Bench agent
* Project: [sympy/sympy](https://github.com/sympy/sympy) · SWE-bench Verified instance sympy__sympy-24213
* Test file: sympy/physics/units/tests/test_quantities.py
* Polluter (agent test): test_collect_factor_and_dimension_with_equivalent_dims_addition — creates Quantity('t1').
* Victim (which goes flaky): test_dimensional_expr_of_derivative.
* Mechanism: Quantity() permanently mutates the global SI registry. Both tests register a quantity named t1, so whichever runs first wins — and the victim becomes order-dependent.
* Proof: renaming the agent's t1 → t1_agent drops the flaky count 4 → 3.

POLLUTER TEST (agent-generated):

```python
def test_collect_factor_and_dimension_with_equivalent_dims_addition():
    from sympy.physics.units import acceleration, velocity, time, meter, second
    v1 = Quantity('v1')
    SI.set_quantity_dimension(v1, velocity)
    SI.set_quantity_scale_factor(v1, 2 * meter / second)

    a1 = Quantity('a1')
    SI.set_quantity_dimension(a1, acceleration)
    SI.set_quantity_scale_factor(a1, -9.8 * meter / second**2)

    t1 = Quantity('t1')                       # collides with the victim test's Quantity('t1')
    SI.set_quantity_dimension(t1, time)
    SI.set_quantity_scale_factor(t1, 5 * second)

    expr = a1 * t1 + v1
    factor, dim = SI._collect_factor_and_dimension(expr)
    from math import isclose
    try:
        numeric_coeff = float((factor / (meter/second)).evalf())
    except Exception:
        numeric_coeff = float(factor)
    assert isclose(numeric_coeff, -47.0, rel_tol=1e-12, abs_tol=1e-12)
    assert SI.get_dimension_system().equivalent_dims(dim, velocity)
```

VICTIM TEST (registers its own t1):

```python
def test_dimensional_expr_of_derivative():
    l = Quantity('l')
    t = Quantity('t')
    t1 = Quantity('t1')                       # collides with the agent test's Quantity('t1')
    l.set_global_relative_scale_factor(36, km)
    t.set_global_relative_scale_factor(1, hour)
    t1.set_global_relative_scale_factor(1, second)
    x = Symbol('x')
    y = Symbol('y')
    f = Function('f')
    dfdx = f(x, y).diff(x, y)
    dl_dt = dfdx.subs({f(x, y): l, x: t, y: t1})
    assert SI.get_dimensional_expr(dl_dt) ==\
        SI.get_dimensional_expr(l / t / t1) ==\
        Symbol("length")/Symbol("time")**2
    assert SI._collect_factor_and_dimension(dl_dt) ==\
        SI._collect_factor_and_dimension(l / t / t1) ==\
        (10, length/time**2)
```

## 8. sphinx-8721 (OD polluter)

* Generator: SWT-Bench agent
* Project: [sphinx-doc/sphinx](https://github.com/sphinx-doc/sphinx) · SWE-bench Verified instance sphinx-doc__sphinx-8721
* Test file: tests/test_ext_viewcode.py
* Polluter (agent test): test_viewcode_does_not_create_epub_pages_by_default.
* Victim (goes flaky): test_viewcode.
* Mechanism: the agent test shares a testroot build directory with test_viewcode; its build leaves cached Sphinx env state (env._viewcode_modules) in the shared dir, so the stable test becomes order-dependent. Proof: move the agent test to another testroot and the victim moves with it (→ test_local_source_files); baseline 0 → with agent 1.

POLLUTER TEST (agent-generated):

```python
@pytest.mark.sphinx(testroot='ext-viewcode')
def test_viewcode_does_not_create_epub_pages_by_default(make_app, app_params):
    # build html to populate env._viewcode_modules
    args, kwargs = app_params
    app_html = make_app('html', *args, **kwargs)
    app_html.build()

    kwargs2 = kwargs.copy()
    kwargs2.update({'srcdir': app_html.srcdir})   # reuses the html srcdir so cached state leaks into the shared testroot
    app_epub = make_app('epub', *args, **kwargs2)
    app_epub.build()

    assert not (app_epub.outdir / '_modules').exists()
```

VICTIM TEST (builds from the shared ext-viewcode testroot):

```python
def test_viewcode(app: SphinxTestApp) -> None:
    shutil.rmtree(app.outdir / '_modules', ignore_errors=True)
    app.build(force_all=True)

    result = check_viewcode_output(app)
    assert 'class="linenos">' not in result
```

## Example of a wrong (not flaky) test, as noted in 3rd point's "generated but incorrect" finding

skywalking ConfigInitializer#initialize. Generator: ChatUniTest (gpt-4o). Project: [apache/skywalking-java](https://github.com/apache/skywalking-java), apm-commons/apm-util. Fails deterministically on a mistaken contract. initialize only sets public static fields keyed by a lowercased dotted path, but the test never sets up such a field, so it tests nothing real and expects an exception that never comes.

GENERATED TEST:

```java
public class ConfigInitializer_initialize_0_0_Test {

    private Properties properties;
    private Class<?> rootConfigType;

    @BeforeEach
    public void setUp() {
        properties = new Properties();
        rootConfigType = MockConfig.class; // MockConfig has no public static fields so initialize does nothing
    }

    @Test
    public void testInitializeWithValidInputs() {
        // vacuous: only asserts that a no-op call does not throw
        assertDoesNotThrow(() -> ConfigInitializer.initialize(properties, rootConfigType));
    }

    @Test
    public void testInitializeWithInvalidInputs() {
        // wrong: initNextLevel on an empty class never throws IllegalAccessException
        assertThrows(IllegalAccessException.class, () -> {
            Method method = ConfigInitializer.class.getDeclaredMethod("initNextLevel", Properties.class, Class.class, ConfigDesc.class);
            method.setAccessible(true);
            method.invoke(null, properties, rootConfigType, new ConfigDesc());
        });
    }

    private static class MockConfig { } // empty, nothing to initialize
    private static class ConfigDesc { } // dummy, not skywalking's real ConfigDesc
}
```
