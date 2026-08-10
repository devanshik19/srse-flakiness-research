package org.snakeyaml.engine.v2.representer;

import org.snakeyaml.engine.v2.api.DumpSettings;
import org.snakeyaml.engine.v2.nodes.Tag;
import org.snakeyaml.engine.v2.representer.StandardRepresenter;
import java.util.HashMap;
import java.util.Map;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Base64;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;
import java.util.regex.Pattern;
import org.snakeyaml.engine.v2.api.RepresentToNode;
import org.snakeyaml.engine.v2.common.FlowStyle;
import org.snakeyaml.engine.v2.common.NonPrintableStyle;
import org.snakeyaml.engine.v2.common.ScalarStyle;
import org.snakeyaml.engine.v2.exceptions.YamlEngineException;
import org.snakeyaml.engine.v2.nodes.Node;
import org.snakeyaml.engine.v2.scanner.StreamReader;

class StandardRepresenter_addClassTag_1_1_Test {

    private StandardRepresenter standardRepresenter;

    private Map<Class<?>, Tag> classTags;

    @BeforeEach
    void setUp() {
        // Initialize the classTags map and StandardRepresenter instance
        classTags = new HashMap<>();
        DumpSettings dumpSettings = createDumpSettings();
        standardRepresenter = new StandardRepresenter(dumpSettings);
        // Use reflection to set the protected field classTags
        try {
            java.lang.reflect.Field field = StandardRepresenter.class.getDeclaredField("classTags");
            field.setAccessible(true);
            field.set(standardRepresenter, classTags);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            fail("Failed to set up the test: " + e.getMessage());
        }
    }

    private DumpSettings createDumpSettings() {
        try {
            Constructor<DumpSettings> constructor = DumpSettings.class.getDeclaredConstructor(boolean.class, boolean.class, Optional.class, org.snakeyaml.engine.v2.serializer.AnchorGenerator.class, Optional.class, Map.class, FlowStyle.class, ScalarStyle.class, NonPrintableStyle.class, org.snakeyaml.engine.v2.schema.Schema.class, boolean.class, boolean.class, boolean.class, int.class, int.class, int.class, String.class, boolean.class, int.class, Map.class, boolean.class, boolean.class);
            constructor.setAccessible(true);
            return constructor.newInstance(false, false, Optional.empty(), null, Optional.empty(), new HashMap<>(), null, null, null, null, false, false, false, 0, 0, 0, "\n", false, 0, new HashMap<>(), false, false);
        } catch (NoSuchMethodException | InstantiationException | IllegalAccessException | InvocationTargetException e) {
            throw new RuntimeException("Failed to create DumpSettings instance: " + e.getMessage(), e);
        }
    }

    @Test
    void testAddClassTag() {
        Class<?> clazz = String.class;
        Tag tag = Tag.STR;
        // Test adding a new class tag
        Tag previousTag = standardRepresenter.addClassTag(clazz, tag);
        assertNull(previousTag, "Previous tag should be null when adding a new tag.");
        assertEquals(tag, classTags.get(clazz), "The tag should be added to the classTags map.");
        // Test replacing an existing class tag
        Tag newTag = Tag.INT;
        previousTag = standardRepresenter.addClassTag(clazz, newTag);
        assertEquals(tag, previousTag, "Previous tag should be returned when replacing an existing tag.");
        assertEquals(newTag, classTags.get(clazz), "The new tag should replace the old tag in the classTags map.");
    }

    @Test
    void testAddClassTagWithNullTag() {
        Class<?> clazz = Integer.class;
        // Test adding a class tag with a null tag, expecting a NullPointerException
        assertThrows(NullPointerException.class, () -> standardRepresenter.addClassTag(clazz, null), "Expected NullPointerException when tag is null.");
    }
}
