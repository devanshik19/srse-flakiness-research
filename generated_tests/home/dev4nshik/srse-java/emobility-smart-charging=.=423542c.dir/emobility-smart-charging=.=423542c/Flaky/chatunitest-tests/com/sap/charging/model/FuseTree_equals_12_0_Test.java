package com.sap.charging.model;

import java.lang.reflect.Field;
import com.sap.charging.model.FuseTree;
import com.sap.charging.model.Fuse;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.ArrayList;
import java.util.List;
import java.util.Stack;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.sap.charging.util.Callback;
import com.sap.charging.util.JSONKeys;
import com.sap.charging.util.JSONSerializable;

public class FuseTree_equals_12_0_Test {

    private FuseTree fuseTree1;

    private FuseTree fuseTree2;

    private FuseTree fuseTree3;

    private Fuse rootFuse1;

    private Fuse rootFuse2;

    private Fuse rootFuse3;

    @BeforeEach
    public void setUp() {
        rootFuse1 = new Fuse(1, 100.0);
        rootFuse2 = new Fuse(2, 100.0);
        rootFuse3 = new Fuse(1, 100.0);
        fuseTree1 = new FuseTree(rootFuse1, 5);
        fuseTree2 = new FuseTree(rootFuse2, 5);
        fuseTree3 = new FuseTree(rootFuse3, 10);
    }

    @Test
    public void testEquals_SameObject() {
        assertTrue(fuseTree1.equals(fuseTree1));
    }

    @Test
    public void testEquals_NullObject() {
        assertFalse(fuseTree1.equals(null));
    }

    @Test
    public void testEquals_DifferentClass() {
        assertFalse(fuseTree1.equals(new Object()));
    }

    @Test
    public void testEquals_DifferentRootFuse() {
        assertFalse(fuseTree1.equals(fuseTree2));
    }

    @Test
    public void testEquals_DifferentNumberChargingStations() {
        assertFalse(fuseTree1.equals(fuseTree3));
    }

    @Test
    public void testEquals_SameAttributes() {
        assertTrue(fuseTree1.equals(new FuseTree(rootFuse1, 5)));
    }

    @Test
    public void testEquals_NullRootFuseInBoth() throws Exception {
        // Using reflection to set private field rootFuse to null
        setPrivateField(fuseTree1, "rootFuse", null);
        setPrivateField(fuseTree2, "rootFuse", null);
        assertTrue(fuseTree1.equals(fuseTree2));
    }

    @Test
    public void testEquals_NullRootFuseInOne() throws Exception {
        // Using reflection to set private field rootFuse to null
        setPrivateField(fuseTree1, "rootFuse", null);
        assertFalse(fuseTree1.equals(fuseTree2));
    }

    private void setPrivateField(Object object, String fieldName, Object value) throws Exception {
        Field field = object.getClass().getDeclaredField(fieldName);
        field.setAccessible(true);
        field.set(object, value);
    }
}
