import unreal
from .ClearLog import ClearLogTool, clear_ue_logs, clear_output_log_only, clear_console_history_only

def register_clear_log_commands():
    """注册清空日志的控制台命令"""
    
    # 注册清空所有日志的命令
    unreal.register_python_console_command(
        "clear_logs",
        "清空UE控制台所有日志",
        lambda: clear_ue_logs()
    )
    
    # 注册仅清空输出日志的命令
    unreal.register_python_console_command(
        "clear_output",
        "仅清空输出日志窗口",
        lambda: clear_output_log_only()
    )
    
    # 注册仅清空控制台历史的命令
    unreal.register_python_console_command(
        "clear_history",
        "仅清空控制台命令历史",
        lambda: clear_console_history_only()
    )
    
    unreal.log("[ClearLog] 已注册清空日志命令:")
    unreal.log("  clear_logs - 清空所有日志")
    unreal.log("  clear_output - 仅清空输出日志")
    unreal.log("  clear_history - 仅清空控制台历史")

def unregister_clear_log_commands():
    """注销清空日志的控制台命令"""
    try:
        unreal.unregister_python_console_command("clear_logs")
        unreal.unregister_python_console_command("clear_output")
        unreal.unregister_python_console_command("clear_history")
        unreal.log("[ClearLog] 已注销清空日志命令")
    except Exception as e:
        unreal.log_warning(f"[ClearLog] 注销命令时出错: {str(e)}")

# 自动注册命令
try:
    register_clear_log_commands()
    unreal.log("[ClearLog] ClearLog工具已加载并注册命令")
except Exception as e:
    unreal.log_error(f"[ClearLog] 加载失败: {str(e)}")