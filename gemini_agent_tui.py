from textual import events, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.suggester import SuggestFromList
from textual.widget import Widget
from textual.widgets import Header, Footer, Input, Label, Markdown, Static, OptionList
from textual.containers import Horizontal, ScrollableContainer, Vertical, Container
from textual.screen import ModalScreen
from gemini import User_Chat, setting
import asyncio, os


class SessionPicker(ModalScreen):

    CSS = """
    ModalScreen {
            align: center middle;
            }
    """

    BINDINGS = [ ("escape", "app.pop_screen", "Close") ]

    def compose(self) -> ComposeResult:
        with Container(id="modal-container"):
            yield Static("Select Model")
            yield OptionList(id='option-list')

    def on_mount(self) -> None:
        option_list = self.query_one("#option-list", OptionList)
        option_list.clear_options()
        for _, _, name in os.walk('chats/'):
            name.sort(reverse=True)
            option_list.add_options(name)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        self.dismiss(event.option.prompt)


class ModelPicker(ModalScreen):

    CSS = """
    ModalScreen {
            align: center middle;
            }
    """

    BINDINGS = [ ("escape", "app.pop_screen", "Close") ]

    def compose(self) -> ComposeResult:
        model_list = OptionList("gemini-2.5-flash",
                                "gemini-2.5-flash-lite",
                                "gemini-3-flash-preview",
                                "gemini-3.1-flash-lite-preview",
                                "gemini-flash-latest",
                                "gemini-flash-lite-latest",
                                "gemma-3-27b-it",
                                "gemma-3-12b-it",
                                "gemma-3-4b-it",
                                "gemma-3-1b-it",
                                "gemma-3n-e4b-it",
                                "gemma-3n-e2b-it",
                                )
        with Container(id="modal-container"):
            yield Static("Select Model")
            yield model_list

    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        self.dismiss(event.option.prompt)


class MainApp(App):

    CSS = """
    .input-bar {
            max-height: 4;
            border: hkey $accent;
            background: $panel;
           }
    #model-name {
            background: $accent;
            color: ansi_black;
            }
    .chat-status {
            height: 1;
            }
    .agent-style {
            margin: 1 0 0 0;
            border: hkey purple;
            }
    .system-style {
            margin: 1 0 0 0;
            border: hkey blue;
            }
    .user-style {
            margin: 1 0 0 0;
            border: hkey $accent;
            }
    .error-style {
            margin: 1 0 0 0;
            border: hkey red;
            }
    #log-container {
            padding: 0 0 1 1;
            }
    """

    BINDINGS = [
            Binding('shift+enter', 'submit', 'Submit user input', show=False)
            ]

    def compose(self) -> ComposeResult:
        command = ['/model', '/quit', '/exit', '/save', '/session', '/new']
        self.commands = SuggestFromList(command, case_sensitive=False)
        self.status = Label("", id="status")
        self.model_lbl = Label("model", id="model-name")
        yield Header(show_clock=True)
        with Vertical():
            with Vertical():
                yield ScrollableContainer(id="log-container")
            # status line
            with Vertical(classes='input-bar'):
                yield Input(placeholder="How can i help you", compact=True, suggester=self.commands)
                with Horizontal(classes="chat-status"):
                    with Horizontal():
                        yield self.status
                    yield self.model_lbl
        yield Footer()

    def initialize_chat(self):
        self.chat = User_Chat()
        self.model_lbl.update(self.chat.current_model)

    def on_mount(self) -> None:
        self.theme = "gruvbox"
        self.title = "Chat"
        log = self.query_one("#log-container")
        self.initialize_chat() 
        log.mount(Label("Gemini Cli lite chat system.\nSystem: Gemini Agent initialized.", classes="system-style"))
        self.query_one(Input).focus()

    @work
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        input_widget = event.input
        log = self.query_one("#log-container", ScrollableContainer)

        user_input = input_widget.value.strip()

        if user_input:
            log.mount(Label(f"➜ You: {user_input}", classes="user-style"))
            input_widget.value = ""

            if user_input.startswith("/"):
                parts = user_input.split(" ", 1)
                command, args = parts[0], parts[1] if len(parts) > 1 else ""

                if command == "/model":
                    result = await self.app.push_screen_wait(ModelPicker())
                    self.chat.change_model(result)
                    self.model_lbl.update(result)
                    log.mount(Label(f"➜ System: Model is changed to '{result}'.", classes="system-style"))
                elif command == "/usage":
                    pass
                elif command == "/save":
                    self.save_chat(args)
                elif command == "/session":
                    self.save_chat(args)
                    file = await self.push_screen_wait(SessionPicker())
                    conversation = self.chat.load_chat(file)
                    await log.remove_children()
                    self.load_chat(conversation)
                elif command == "/new":
                    self.save_chat(args)
                    self.chat.new_chat()
                    await log.remove_children()
                    log.mount(Label("Gemini Cli lite chat system.\nSystem: Gemini Agent initialized.", classes="system-style"))
                elif command == "/quit" or command == "/exit":
                    self.app.exit()
                else:
                    log.mount(Label(f"➜ System:  Unknown command '{command}'.", classes="system-style"))
            else:
                self.status.update("Processing...")
                await self.send_input(user_input)
                self.status.update("Done..")

    def save_chat(self, args):
        file = self.chat.save_chat(args);
        if file:
            self.notify(f"Chat has been saved to {file}")
   
    def load_chat(self, chat):
        log = self.query_one("#log-container", ScrollableContainer)
        for data in chat:
            if data['role'] == "user":
                user_input = ''
                for text in data['parts']:
                    user_input+=text['text']
                log.mount(Label(f"➜ You: {user_input}", classes='user-style'))
            elif data['role'] == "model":
                response = ''
                for text in data['parts']:
                    response+=text['text']
                log.mount(Markdown(response, classes="agent-style"))
               
    async def send_input(self, message):
        loop = asyncio.get_running_loop()
        try:
            response = await loop.run_in_executor(None, self.chat.call_chat, message)
            if response:
                self.query_one("#log-container").mount(Markdown(response, classes="agent-style"))
        except Exception as e:
                self.query_one("#log-container").mount(Label(str(e), classes='error-style'))
             

if __name__ == "__main__":
    MainApp().run()

