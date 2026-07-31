import unreal
import sys

class ClearLogTool:
    """UE控制台日志清理工具"""
    
    def __init__(self):
        self.output_log = unreal.get_editor_subsystem(unreal.OutputLog)
        self.console_command_system = unreal.get_editor_subsystem(unreal.ConsoleCommandSubsystem)
    
    def clear_output_log(self):
        """清空输出日志窗口"""
        try:
            if self.output_log:
                # 方法1: 使用OutputLog的clear方法
                self.output_log.clear()
                unreal.log("[ClearLog] 输出日志已清空")
                return True
            else:
                unreal.log_warning("[ClearLog] 无法获取OutputLog子系统")
                return False
        except Exception as e:
            unreal.log_error(f"[ClearLog] 清空输出日志失败: {str(e)}")
            return False
    
    def clear_console_history(self):
        """清空控制台命令历史"""
        try:
            # 使用控制台命令清空历史
            if self.console_command_system:
                self.console_command_system.execute_console_command("Console.History.Clear")
                unreal.log("[ClearLog] 控制台历史已清空")
                return True
            else:
                unreal.log_warning("[ClearLog] 无法获取ConsoleCommandSubsystem")
                return False
        except Exception as e:
            unreal.log_error(f"[ClearLog] 清空控制台历史失败: {str(e)}")
            return False
    
    def clear_all_logs(self):
        """清空所有日志相关内容"""
        unreal.log("[ClearLog] 开始清理日志...")
        
        success_output = self.clear_output_log()
        success_console = self.clear_console_history()
        
        # 额外的清理：使用控制台命令
        try:
            unreal.SystemLibrary.execute_console_command(unreal.get_editor_world(), "clear")
            unreal.log("[ClearLog] 控制台命令执行完成")
        except Exception as e:
            unreal.log_warning(f"[ClearLog] 控制台命令执行失败: {str(e)}")
        
        if success_output and success_console:
            unreal.log("[ClearLog] 所有日志清理完成！")
            return True
        else:
            unreal.log_warning("[ClearLog] 部分清理操作失败")
            return False
    
    def get_log_info(self):
        """获取当前日志信息"""
        try:
            if self.output_log:
                # 尝试获取日志信息（不同UE版本可能有不同方法）
                unreal.log("[ClearLog] 当前日志系统信息:")
                unreal.log(f"  OutputLog子系统: {'可用' if self.output_log else '不可用'}")
                unreal.log(f"  ConsoleCommandSubsystem: {'可用' if self.console_command_system else '不可用'}")
                return True
            else:
                unreal.log_warning("[ClearLog] 无法获取日志信息")
                return False
        except Exception as e:
            unreal.log_error(f"[ClearLog] 获取日志信息失败: {str(e)}")
            return False

def main():
    """主函数"""
    try:
        # 创建清理工具实例
        clear_tool = ClearLogTool()
        
        # 显示当前日志信息
        clear_tool.get_log_info()
        
        # 执行清理
        result = clear_tool.clear_all_logs()
        
        if result:
            unreal.log("[ClearLog] 脚本执行成功")
        else:
            unreal.log_warning("[ClearLog] 脚本执行部分失败")
            
    except Exception as e:
        unreal.log_error(f"[ClearLog] 脚本执行异常: {str(e)}")

# 如果直接运行此脚本，执行main函数
if __name__ == "__main__":
    main()

# 提供便捷函数供其他脚本调用
def clear_ue_logs():
    """便捷函数：清空UE日志"""
    clear_tool = ClearLogTool()
    return clear_tool.clear_all_logs()

def clear_output_log_only():
    """便捷函数：仅清空输出日志"""
    clear_tool = ClearLogTool()
    return clear_tool.clear_output_log()

def clear_console_history_only():
    """便捷函数：仅清空控制台历史"""
    clear_tool = ClearLogTool()
    return clear_tool.clear_console_history()