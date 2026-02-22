import time
import sys
import random
import threading

# --- 🎨 Color Palette (Neurodivergent-Friendly) ---
COLORS = {
    'bg_dark': '\033[48;2;15;23;42m',      # #0f172a
    'bg_card': '\033[48;2;30;41;59m',      # #1e293b
    'text': '\033[38;2;241;245;249m',      # #f1f5f9
    'dim': '\033[38;2;148;163;184m',       # #94a3b8
    'accent': '\033[38;2;56;189;248m',     # #38bdf8
    'success': '\033[38;2;34;197;94m',     # #22c55e
    'warning': '\033[38;2;245;158;11m',    # #f59e0b
    'error': '\033[38;2;239;68;68m',       # #ef4444
    'reset': '\033[0m'
}

# --- 🟢 Status Indicators ---
STATUS = {
    'active': f"{COLORS['success']}🟢{COLORS['reset']}",
    'working': f"{COLORS['warning']}🟡{COLORS['reset']}",
    'error': f"{COLORS['error']}🔴{COLORS['reset']}",
    'idle': f"{COLORS['dim']}⚪{COLORS['reset']}"
}

def clear_screen():
    print("\033[2J\033[H", end="")

def draw_header():
    print(f"{COLORS['bg_dark']}{' ' * 80}{COLORS['reset']}")
    print(f"{COLORS['bg_dark']}  🧠 {COLORS['accent']}HYPERSWARM{COLORS['text']} Control Center {COLORS['dim']}|{COLORS['text']} Flow: {COLORS['success']}HYPERFOCUS ⚡ {COLORS['bg_dark']}{' ' * 28}{COLORS['reset']}")
    print(f"{COLORS['bg_dark']}{' ' * 80}{COLORS['reset']}")
    print("")

def draw_card(title, content_lines, width=40):
    border = f"{COLORS['dim']}─{COLORS['reset']}"
    print(f"{COLORS['dim']}┌{'─' * (width-2)}┐{COLORS['reset']}")
    print(f"{COLORS['dim']}│{COLORS['reset']} {COLORS['accent']}{title:<{width-4}}{COLORS['reset']} {COLORS['dim']}│{COLORS['reset']}")
    print(f"{COLORS['dim']}├{'─' * (width-2)}┤{COLORS['reset']}")
    for line in content_lines:
        # Strip ANSI for length calc (simplified)
        clean_line = line.replace(COLORS['success'], '').replace(COLORS['warning'], '').replace(COLORS['error'], '').replace(COLORS['reset'], '').replace(COLORS['dim'], '').replace(COLORS['accent'], '')
        padding = width - 4 - len(clean_line)
        # Note: This simple padding calc fails with ANSI codes, so we just print directly for demo
        print(f"{COLORS['dim']}│{COLORS['reset']} {line} {COLORS['dim']}{' ' * padding}│{COLORS['reset']}") 
    print(f"{COLORS['dim']}└{'─' * (width-2)}┘{COLORS['reset']}")

def simulate_activity():
    activities = [
        f"{STATUS['active']} PHOENIX: Monitoring system health...",
        f"{STATUS['working']} ARCHITECT: Refactoring API schema...",
        f"{STATUS['idle']} RESEARCHER: Awaiting task...",
        f"{STATUS['active']} CFO: Budget optimization active ($3.47)",
        f"{STATUS['error']} QA: Test failed in module auth.py"
    ]
    return activities

def animated_loader(duration=3):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{COLORS['accent']}{frames[i % len(frames)]} Processing intent...{COLORS['reset']}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print(f"\r{COLORS['success']}✅ Intent processed successfully!{COLORS['reset']}   ")

def main():
    clear_screen()
    draw_header()
    
    # 1. Visual Cortex / Agent Mesh
    print(f"{COLORS['text']}🎯 VISUAL CORTEX (Agent Mesh){COLORS['reset']}")
    print(f"   {STATUS['active']} PHOENIX  ───  {STATUS['working']} ARCHITECT")
    print(f"       │                 │")
    print(f"   {STATUS['idle']} RESEARCHER      {STATUS['active']} CFO")
    print("")

    # 2. Activity Log Card
    logs = simulate_activity()
    draw_card("📋 ACTIVITY LOG", logs, width=50)
    print("")

    # 3. Cost Tracker
    costs = [
        f"Today:    {COLORS['accent']}$3.47{COLORS['reset']}",
        f"Week:     {COLORS['accent']}$18.24{COLORS['reset']}",
        f"Last Ops: {COLORS['success']}$0.02{COLORS['reset']}"
    ]
    draw_card("💰 COST TRACKER", costs, width=50)
    print("")

    # 4. Intent Input (Interactive)
    print(f"{COLORS['dim']}┌{'─' * 48}┐{COLORS['reset']}")
    print(f"{COLORS['dim']}│{COLORS['reset']} 💭 {COLORS['text']}INTENT BOX{COLORS['reset']}{' ' * 33}{COLORS['dim']}│{COLORS['reset']}")
    print(f"{COLORS['dim']}│{COLORS['reset']} {COLORS['dim']}Type your goal (e.g., 'Fix API latency'){COLORS['reset']}{' ' * 8}{COLORS['dim']}│{COLORS['reset']}")
    print(f"{COLORS['dim']}└{'─' * 48}┘{COLORS['reset']}")
    
    try:
        user_input = input(f"\n{COLORS['accent']}>> {COLORS['reset']}")
        if user_input:
            print("")
            animated_loader()
            print(f"\n{COLORS['dim']}Action dispatched to {COLORS['accent']}ARCHITECT{COLORS['dim']} and {COLORS['accent']}PHOENIX{COLORS['reset']}")
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()
