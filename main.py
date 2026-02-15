from reader import save_report
from reporter import analyze_log, generate_report

def main():
    """פונקציה להפעלה התוכנית"""
    suspicious = analyze_log("network_traffic.log")

    report = generate_report(suspicious)

    print(report)

    save_report(report, "security_report.txt")

if __name__ == '__main__':
    main()