import unreal
from threading import Timer

@unreal.uclass()
class Notification(unreal.EditorUtilityTask):
    pass

class EditorPrompt:

    @staticmethod
    def show_notification(message, time=1.0):
        
        def update_notification(notification, message):
            notification.set_task_notification_text(str(message))
            # notification.finish_executing_task()

        def create_notification(message):
            notification = Notification()
            util_subsystem = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem)
            notification.receive_begin_execution()
            util_subsystem.register_and_execute_task(notification)
            notification.set_task_notification_text(str(message))
            return notification
        
        def finish_notification(notification):
            notification.finish_executing_task()

        notification = create_notification(message)
        # t = Timer(time, lambda: update_notification(notification, "count3"))
        # t.start()
        te = Timer(3.0, lambda: finish_notification(notification))
        te.start()

    @staticmethod
    def show_modal_warning(message, title="Warning", buttons=unreal.AppMsgType.OK):
        unreal.EditorDialog.show_message(
            title,
            message,
            buttons
        )

    @staticmethod
    def show_modal(title, message, buttons=unreal.AppMsgType.OK):
        """显示模态对话框"""
        return unreal.EditorDialog.show_message(title, message, buttons)

    @staticmethod 
    def show_tool_tip(text, timeout=2.0):
        """显示工具提示"""
        mouse_position = unreal.EditorLibrary.get_mouse_position()
        unreal.EditorDialog.show_tool_tip(mouse_position, text, timeout)