
import org.junit.platform.launcher.Launcher;
import org.junit.platform.launcher.LauncherDiscoveryRequest;
import org.junit.platform.launcher.core.LauncherDiscoveryRequestBuilder;
import org.junit.platform.launcher.core.LauncherFactory;
import org.junit.platform.launcher.listeners.SummaryGeneratingListener;
import org.junit.platform.launcher.listeners.TestExecutionSummary;
import static org.junit.platform.engine.discovery.DiscoverySelectors.selectMethod;

public class FlakyCheckNio5 {
    public static void main(String[] a) throws Exception {
        for (int i = 1; i <= 2; i++) {
            LauncherDiscoveryRequest req = LauncherDiscoveryRequestBuilder.request()
                .selectors(selectMethod(a[0], a[1])).build();
            Launcher launcher = LauncherFactory.create();
            SummaryGeneratingListener listener = new SummaryGeneratingListener();
            launcher.execute(req, listener);
            TestExecutionSummary s = listener.getSummary();
            String why = s.getFailures().isEmpty() ? "" : String.valueOf(s.getFailures().get(0).getException());
            String outcome = s.getTestsStartedCount() == 0 ? "NOTRUN" : s.getTotalFailureCount() > 0 ? "FAIL" : "PASS";
            System.out.println("FLAKYCHECK_NIO " + i + " " + outcome + " " + why.replace('\n', ' '));
        }
        System.exit(0);
    }
}
