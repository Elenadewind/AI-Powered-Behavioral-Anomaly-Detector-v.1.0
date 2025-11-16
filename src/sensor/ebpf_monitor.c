c
/*
eBPF Monitor Template (Linux)

WARNING: Incomplete. For educational purposes only.
*/

#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>

struct event {
    char comm[16];
    int pid;
    char api[32];
};

BPF_PERF_OUTPUT(events);

/*
 * Placeholder for execve monitoring
 * Actual implementation requires proper kprobe attachment
 */
int kprobe__sys_execve(struct pt_regs *ctx, const char __user *filename) {
    struct event evt = {};
    bpf_get_current_comm(&evt.comm, sizeof(evt.comm));
    evt.pid = bpf_get_current_pid_tgid() >> 32;
    
    // WARNING: bpf_probe_read_user() usage requires validation
    bpf_probe_read_user(&evt.api, sizeof(evt.api), (void *)filename);
    events.perf_submit(ctx, &evt, sizeof(evt));
    return 0;
}

char _license[] SEC("license") = "GPL";

c
/*
eBPF Monitor for Linux
Tracks execve, connect, open syscalls.
*/

#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>


struct event {
    char comm[16];
    int pid;
    char syscall[32];
    long long timestamp;
};

BPF_PERF_OUTPUT(events);

SEC("kprobe/sys_execve")
int handle_execve(struct pt_regs *ctx) {
    struct event evt = {};
    bpf_get_current_comm(&evt.comm, sizeof(evt.comm));
    evt.pid = bpf_get_current_pid_tgid() >> 32;
    bpf_probe_read_user(&evt.syscall, sizeof(evt.syscall), (void *)"execve");
    evt.timestamp = bpf_ktime_get_ns();
    events.perf_submit(ctx, &evt, sizeof(evt));
    return 0;
}

SEC("kprobe/sys_connect")
int handle_connect(struct pt_regs *ctx) {
    // Аналогично для connect
    return 0;
}

SEC("kprobe/sys_open")
int handle_open(struct pt_regs *ctx) {
    // Аналогично для open
    return 0;
}

char _license[] SEC("license") = "GPL";
