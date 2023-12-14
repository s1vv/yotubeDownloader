import wx
import wx.xrc
import wx.richtext
from pytube import YouTube
from pytube import Playlist
from tqdm import tqdm


class MyFrame1(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition,
                          size=wx.Size(600, 400), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.m_menubar2 = wx.MenuBar(0)
        self.file_m = wx.Menu()
        self.exit_item = wx.MenuItem(self.file_m, wx.ID_ANY, u"Выход\tCtrl+Q", wx.EmptyString, wx.ITEM_NORMAL)
        self.file_m.Append(self.exit_item)

        self.m_menubar2.Append(self.file_m, u"Файл")

        self.help_m = wx.Menu()

        self.help_item = wx.MenuItem(self.help_m, wx.ID_ANY, u"О программе", wx.EmptyString, wx.ITEM_NORMAL)
        self.help_m.Append(self.help_item)

        self.m_menubar2.Append(self.help_m, u"Как скачать")

        self.SetMenuBar(self.m_menubar2)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.txt_lnk = wx.StaticText(self, wx.ID_ANY, u"Вставьте ссылку на видео или playlist", wx.DefaultPosition,
                                     wx.DefaultSize, 0)
        self.txt_lnk.Wrap(-1)

        bSizer2.Add(self.txt_lnk, 0, wx.ALL, 5)

        self.lnk_txtctrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.lnk_txtctrl, 0, wx.ALL | wx.EXPAND, 5)

        self.only_audio_check = wx.CheckBox(self, wx.ID_ANY, u"Скачать только аудио", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        bSizer2.Add(self.only_audio_check, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.bt_done = wx.Button(self, wx.ID_ANY, u"Готово", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.bt_done, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        bSizer1.Add(bSizer2, 0, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"Выберите поток (разрешение, формат)", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)

        bSizer4.Add(self.m_staticText4, 0, wx.ALL, 5)

        self.choiceChoices = ['', '', '', '', '', '', '', '', '', '']
        self.choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.choiceChoices, 0)
        self.choice.SetSelection(0)
        bSizer4.Add(self.choice, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, u"Сохранить в папку", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)

        bSizer4.Add(self.m_staticText5, 0, wx.ALL, 5)

        self.dir = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition,
                                    wx.DefaultSize, wx.DIRP_DEFAULT_STYLE)
        bSizer4.Add(self.dir, 0, wx.ALL | wx.EXPAND, 5)

        self.bt_start = wx.Button(self, wx.ID_ANY, u"Скачать", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.bt_start, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        bSizer1.Add(bSizer4, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_MENU, self.on_quit, id=self.exit_item.GetId())
        self.Bind(wx.EVT_MENU, self.help_download, id=self.help_item.GetId())
        self.bt_done.Bind(wx.EVT_BUTTON, self.on_done)
        self.bt_start.Bind(wx.EVT_BUTTON, self.start)

    # Virtual event handlers, override them in your derived class

    def on_quit(self, event):
        self.Close()

    def help_download(self, event):
        dlg = DialogInfo(None)
        dlg.ShowModal()

    def on_done(self, event):
        for n, val_none in enumerate(['' for z in range(10)]):
            self.choice.SetString(n, val_none)
        if 'https://youtu.be/' in self.lnk_txtctrl.GetValue():

            print('Получение списка потоков: ', self.lnk_txtctrl.GetValue())
            yt = YouTube(self.lnk_txtctrl.GetValue())
            if self.only_audio_check.GetValue():
                STREAMS.clear()
                list_streams = yt.streams.filter(only_audio=True)
                for count, valt in enumerate(tqdm(list_streams)):
                    self.choice.SetString(count, str(valt))
                    STREAMS.append(str(valt))

            else:
                STREAMS.clear()
                list_streams = yt.streams.filter(file_extension='mp4')
                for count, valt in enumerate(tqdm(list_streams)):
                    self.choice.SetString(count, str(valt))
                    STREAMS.append(str(valt))

        elif 'https://youtube.com/playlist?list=' in self.lnk_txtctrl.GetValue():
            pl = Playlist(self.lnk_txtctrl.GetValue())
            print('Загрузка медиа из play list', pl)
            if self.only_audio_check.GetValue():
                for t in tqdm(pl):
                    try:
                        st = (YouTube(str(t)).streams.filter(only_audio=True, bitrate='128kbps').
                              last().download(output_path=self.dir.GetPath()))

                    except Exception as err:
                        print('Ошибка:', err)
                        dlg = MyDialog3(None)
                        dlg.ShowModal()
            else:
                for t in tqdm(pl):
                    try:
                        st = (YouTube(str(t)).streams.filter(progressive=True, file_extension='mp4').
                              order_by('resolution').last().download(output_path=self.dir.GetPath()))
                    except Exception as err:
                        print('Ошибка:', err)
                        dlg = MyDialog3(None)
                        dlg.ShowModal()


    def start(self, event):
        try:
            # print(STREAMS)
            # value = STREAMS[self.choice.GetSelection()]
            # print(value)
            yt = YouTube(self.lnk_txtctrl.GetValue())
            stream = yt.streams.get_by_itag(int(STREAMS[self.choice.GetSelection()].
                                                split('\"')[1])).download(output_path=self.dir.GetPath())
        except Exception as err:
            print('Ошибка:', err)

        done = Done(None)
        done.ShowModal()
# https://youtube.com/playlist?list=PLA0M1Bcd0w8wd5aJ8uUgrFmK_wyqg97j9&si=7-rVoGy43aXtcoi8

class DialogInfo(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                           size=wx.Size(550, 220), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        self.m_richText1 = wx.richtext.RichTextCtrl(self, wx.ID_ANY,
                                                    u"YouTubeDownloader beta - программа для скачивания контента из YouTube."
                                                    "\nБольше информации на сайте: 89301609912.ru\ne-mail: 89301609912@mail.ru"
                                                    "\nДонат можно сделать на номер 89301609912 через СБП в банк КИВИ (Qiwi)"
                                                    "\nДля скачивания видео со звуком выбирайте поток c двухзначным параметром itag (например itag=\"22\")"
                                                    "\nСкачивание плей листов происходит автоматически в разрешении 720р (HD)"
                                                    "\nвставили ссылку, выбрали папку для сохранения нажали ГОТОВО - скачивание началось",
                                                    wx.DefaultPosition, wx.DefaultSize,
                                                    0 | wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER | wx.WANTS_CHARS)
        bSizer6.Add(self.m_richText1, 1, wx.EXPAND | wx.ALL, 5)

        self.bt_ok = wx.Button(self, wx.ID_ANY, u"Да", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer6.Add(self.bt_ok, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(bSizer6)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.bt_ok.Bind(wx.EVT_BUTTON, self.bt_okOnButtonClick)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    # Virtual event handlers, override them in your derived class
    def bt_okOnButtonClick(self, event):
        self.Destroy()

    def on_close(self, event):
        self.Destroy()


class MyDialog3(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                           size=wx.Size(200, 100), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"Поток не доступен", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)

        bSizer8.Add(self.m_staticText4, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button5 = wx.Button(self, wx.ID_ANY, u"Продолжить", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer8.Add(self.m_button5, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(bSizer8)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button5.Bind(wx.EVT_BUTTON, self.m_button5OnButtonClick)

    # Virtual event handlers, override them in your derived class
    def m_button5OnButtonClick(self, event):
        self.Destroy()

class Done(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                           size=wx.Size(200, 100), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"Поток скачан", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)

        bSizer8.Add(self.m_staticText4, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button5 = wx.Button(self, wx.ID_ANY, u"Продолжить", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer8.Add(self.m_button5, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(bSizer8)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button5.Bind(wx.EVT_BUTTON, self.m_button5OnButtonClick)

    # Virtual event handlers, override them in your derived class
    def m_button5OnButtonClick(self, event):
        self.Destroy()


if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame1(None, 'YouTubeDownloader')
    frame.Show()
    PLAYLIST = []
    STREAMS = []
    app.MainLoop()
