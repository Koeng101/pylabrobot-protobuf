package main

import (
	"bufio"
	"context"
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"syscall"
	"testing"
	"time"

	"connectrpc.com/connect"

	starv1 "github.com/PyLabRobot/pylabrobot-protobuf/src/client/go/gen/star/v1"
	"github.com/PyLabRobot/pylabrobot-protobuf/src/client/go/gen/star/v1/starv1connect"
)

const testPort = 18770

var client starv1connect.STARServiceClient

// repoRoot returns the repository root by walking up from this test file.
func repoRoot() string {
	_, filename, _, _ := runtime.Caller(0)
	// src/client/go/star_lifecycle_test.go -> repo root is 3 levels up
	return filepath.Join(filepath.Dir(filename), "..", "..", "..")
}

func TestMain(m *testing.M) {
	root := repoRoot()
	pythonBin := filepath.Join(root, ".venv", "bin", "python")
	script := filepath.Join(root, "scripts", "start_test_server.py")

	cmd := exec.Command(pythonBin, script, "--port", fmt.Sprintf("%d", testPort))
	cmd.Stderr = os.Stderr

	stdout, err := cmd.StdoutPipe()
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to create stdout pipe: %v\n", err)
		os.Exit(1)
	}

	if err := cmd.Start(); err != nil {
		fmt.Fprintf(os.Stderr, "failed to start test server: %v\n", err)
		os.Exit(1)
	}

	// Wait for READY sentinel.
	scanner := bufio.NewScanner(stdout)
	ready := false
	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, "READY") {
			ready = true
			break
		}
	}
	if !ready {
		fmt.Fprintf(os.Stderr, "test server did not become ready\n")
		cmd.Process.Signal(syscall.SIGINT)
		cmd.Wait()
		os.Exit(1)
	}

	// Health poll: make sure HTTP is actually accepting connections.
	baseURL := fmt.Sprintf("http://127.0.0.1:%d", testPort)
	deadline := time.Now().Add(5 * time.Second)
	for time.Now().Before(deadline) {
		resp, err := http.Get(baseURL)
		if err == nil {
			resp.Body.Close()
			break
		}
		time.Sleep(100 * time.Millisecond)
	}

	client = starv1connect.NewSTARServiceClient(http.DefaultClient, baseURL)

	code := m.Run()

	cmd.Process.Signal(syscall.SIGINT)
	cmd.Wait()

	os.Exit(code)
}

func TestGetNumChannels(t *testing.T) {
	resp, err := client.GetNumChannels(context.Background(),
		connect.NewRequest(&starv1.GetNumChannelsRequest{}))
	if err != nil {
		t.Fatalf("GetNumChannels: %v", err)
	}
	if got := resp.Msg.NumChannels; got != 8 {
		t.Errorf("num_channels = %d, want 8", got)
	}
}

func TestGetIswapInstalled(t *testing.T) {
	resp, err := client.GetIswapInstalled(context.Background(),
		connect.NewRequest(&starv1.GetIswapInstalledRequest{}))
	if err != nil {
		t.Fatalf("GetIswapInstalled: %v", err)
	}
	if !resp.Msg.Installed {
		t.Error("iswap_installed = false, want true")
	}
}

func TestGetHead96Installed(t *testing.T) {
	resp, err := client.GetHead96Installed(context.Background(),
		connect.NewRequest(&starv1.GetHead96InstalledRequest{}))
	if err != nil {
		t.Fatalf("GetHead96Installed: %v", err)
	}
	if !resp.Msg.Installed {
		t.Error("head96_installed = false, want true")
	}
}

func TestGetIswapParked(t *testing.T) {
	resp, err := client.GetIswapParked(context.Background(),
		connect.NewRequest(&starv1.GetIswapParkedRequest{}))
	if err != nil {
		t.Fatalf("GetIswapParked: %v", err)
	}
	if !resp.Msg.Parked {
		t.Error("iswap_parked = false, want true")
	}
}

func TestGetCoreParked(t *testing.T) {
	resp, err := client.GetCoreParked(context.Background(),
		connect.NewRequest(&starv1.GetCoreParkedRequest{}))
	if err != nil {
		t.Fatalf("GetCoreParked: %v", err)
	}
	if !resp.Msg.Parked {
		t.Error("core_parked = false, want true")
	}
}
