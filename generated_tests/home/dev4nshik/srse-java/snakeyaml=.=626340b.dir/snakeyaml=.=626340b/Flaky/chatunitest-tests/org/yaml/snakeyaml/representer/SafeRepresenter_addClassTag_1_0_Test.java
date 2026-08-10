package org.yaml.snakeyaml.representer;

import org.yaml.snakeyaml.nodes.Tag;
import org.yaml.snakeyaml.representer.SafeRepresenter;
import java.util.HashMap;
import java.util.Map;
import org.yaml.snakeyaml.DumperOptions;
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
import java.util.Calendar;
import java.util.Date;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Set;
import java.util.TimeZone;
import java.util.UUID;
import java.util.regex.Pattern;
import org.yaml.snakeyaml.error.YAMLException;
import org.yaml.snakeyaml.external.biz.base64Coder.Base64Coder;
import org.yaml.snakeyaml.nodes.Node;
import org.yaml.snakeyaml.reader.StreamReader;

class SafeRepresenter_addClassTag_1_0_Test {

    private SafeRepresenter safeRepresenter;

    @BeforeEach
    void setUp() {
        DumperOptions dumperOptions = new DumperOptions();
        safeRepresenter = new SafeRepresenter(dumperOptions);
        // Initialize the classTags map using reflection since it's protected
        try {
            java.lang.reflect.Field classTagsField = SafeRepresenter.class.getDeclaredField("classTags");
            classTagsField.setAccessible(true);
            classTagsField.set(safeRepresenter, new HashMap<Class<?>, Tag>());
        } catch (NoSuchFieldException | IllegalAccessException e) {
            fail("Failed to set up test: " + e.getMessage());
        }
    }

    @Test
    void testAddClassTagSuccessfullyAddsTag() {
        Class<?> clazz = String.class;
        Tag tag = new Tag("tag:yaml.org,2002:str");
        Tag previousTag = safeRepresenter.addClassTag(clazz, tag);
        assertNull(previousTag, "No previous tag should exist for this class.");
        try {
            java.lang.reflect.Field classTagsField = SafeRepresenter.class.getDeclaredField("classTags");
            classTagsField.setAccessible(true);
            Map<Class<?>, Tag> classTags = (Map<Class<?>, Tag>) classTagsField.get(safeRepresenter);
            assertEquals(tag, classTags.get(clazz), "The tag should be added for the class.");
        } catch (NoSuchFieldException | IllegalAccessException e) {
            fail("Failed to access classTags field: " + e.getMessage());
        }
    }

    @Test
    void testAddClassTagReplacesExistingTag() {
        Class<?> clazz = Integer.class;
        Tag initialTag = new Tag("tag:yaml.org,2002:int");
        Tag newTag = new Tag("tag:yaml.org,2002:number");
        safeRepresenter.addClassTag(clazz, initialTag);
        Tag previousTag = safeRepresenter.addClassTag(clazz, newTag);
        assertEquals(initialTag, previousTag, "The previous tag should be returned.");
        try {
            java.lang.reflect.Field classTagsField = SafeRepresenter.class.getDeclaredField("classTags");
            classTagsField.setAccessible(true);
            Map<Class<?>, Tag> classTags = (Map<Class<?>, Tag>) classTagsField.get(safeRepresenter);
            assertEquals(newTag, classTags.get(clazz), "The tag should be replaced for the class.");
        } catch (NoSuchFieldException | IllegalAccessException e) {
            fail("Failed to access classTags field: " + e.getMessage());
        }
    }

    @Test
    void testAddClassTagWithNullTagThrowsException() {
        Class<?> clazz = Double.class;
        NullPointerException exception = assertThrows(NullPointerException.class, () -> {
            safeRepresenter.addClassTag(clazz, null);
        });
        assertEquals("Tag must be provided.", exception.getMessage());
    }
}
