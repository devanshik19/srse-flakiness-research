package com.sap.oss.phosphor.fosstars.data.artifact;

import com.sap.oss.phosphor.fosstars.data.artifact.VulnerabilitiesFromOwaspDependencyCheck;
import com.sap.oss.phosphor.fosstars.data.owasp.model.Dependency;
import com.sap.oss.phosphor.fosstars.data.owasp.model.OwaspDependencyCheckEntry;
import com.sap.oss.phosphor.fosstars.data.owasp.model.OwaspDependencyCheckVuln;
import com.sap.oss.phosphor.fosstars.model.Subject;
import com.sap.oss.phosphor.fosstars.model.ValueSet;
import com.sap.oss.phosphor.fosstars.model.feature.oss.OssFeatures;
import com.sap.oss.phosphor.fosstars.model.subject.oss.MavenArtifact;
import com.sap.oss.phosphor.fosstars.model.value.Vulnerabilities;
import java.io.IOException;
import java.util.Collections;
import java.util.Optional;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import static com.sap.oss.phosphor.fosstars.model.Subject.cast;
import static com.sap.oss.phosphor.fosstars.model.feature.oss.OssFeatures.VULNERABILITIES_IN_ARTIFACT;
import static com.sap.oss.phosphor.fosstars.model.other.Utils.setOf;
import com.sap.oss.phosphor.fosstars.data.DataProvider;
import com.sap.oss.phosphor.fosstars.data.NoValueCache;
import com.sap.oss.phosphor.fosstars.data.UserCallback;
import com.sap.oss.phosphor.fosstars.data.ValueCache;
import com.sap.oss.phosphor.fosstars.data.owasp.model.OwaspDependencyCheckReference;
import com.sap.oss.phosphor.fosstars.data.owasp.model.Software;
import com.sap.oss.phosphor.fosstars.data.owasp.model.VulnerableSoftware;
import com.sap.oss.phosphor.fosstars.model.Feature;
import com.sap.oss.phosphor.fosstars.model.value.CVSS;
import com.sap.oss.phosphor.fosstars.model.value.CVSS.V2;
import com.sap.oss.phosphor.fosstars.model.value.CVSS.V3;
import com.sap.oss.phosphor.fosstars.model.value.Reference;
import com.sap.oss.phosphor.fosstars.model.value.VersionRange;
import com.sap.oss.phosphor.fosstars.model.value.Vulnerability;
import com.sap.oss.phosphor.fosstars.model.value.Vulnerability.Builder;
import com.sap.oss.phosphor.fosstars.model.value.Vulnerability.Resolution;
import com.sap.oss.phosphor.fosstars.util.Json;
import java.io.File;
import java.io.FileOutputStream;
import java.net.MalformedURLException;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;
import org.apache.http.HttpEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.owasp.dependencycheck.Engine;
import org.owasp.dependencycheck.exception.ExceptionCollection;
import org.owasp.dependencycheck.exception.ReportException;
import org.owasp.dependencycheck.utils.Settings;
import org.mockito.*;
import org.junit.jupiter.api.*;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
public class VulnerabilitiesFromOwaspDependencyCheck_update_5_0_Test {

    private VulnerabilitiesFromOwaspDependencyCheck dataProvider;

    private MavenArtifact artifact;

    private ValueSet values;

    @BeforeEach
    public void setUp() {
        dataProvider = new VulnerabilitiesFromOwaspDependencyCheck();
        artifact = mock(MavenArtifact.class);
        values = mock(ValueSet.class);
    }

    @Test
    public void testUpdateWithNullValues() {
        assertThrows(NullPointerException.class, () -> dataProvider.update(artifact, null));
    }

    @Test
    public void testUpdateWithNoVersion() {
        when(artifact.version()).thenReturn(Optional.empty());
        assertThrows(IOException.class, () -> dataProvider.update(artifact, values));
    }

    @Test
    public void testUpdateWithNoDependencies() throws Exception {
        when(artifact.version()).thenReturn(Optional.of("1.0.0"));
        VulnerabilitiesFromOwaspDependencyCheck spyProvider = spy(dataProvider);
        doReturn(Optional.empty()).when(spyProvider).scan(artifact);
        spyProvider.update(artifact, values);
        verify(values).update(VULNERABILITIES_IN_ARTIFACT.unknown());
    }
}
