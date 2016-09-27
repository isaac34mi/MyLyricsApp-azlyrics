import kivy
kivy.require('1.9.1') # replace with your current kivy version !
from bs4 import BeautifulSoup
import urllib2

from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width','400')			#setting the width of the app when started 
Config.set('graphics', 'height','400')			#setting the height of the app when started 
from kivy.uix.button import Button				#importing the Button widget
from kivy.uix.label import Label				#importing the Label widget
from kivy.uix.boxlayout import BoxLayout		#this will be used arranging the widget on the screen
from kivy.uix.textinput import TextInput		#import a text-input for user input and display.

""" This is a simple app that is created using kivy. Kivy is an open-source python library for repid development of application
	that make use of innovating user interfaces and its also cross paltform.(https://kivy.org/docs/gettingstarted/intro.html)
	This app is an A-z lyrics app. I called it 'A-z lyrics app' because the lyrics are from http://www.azlyrics.com.
	This app is for educational and desmostration purposes only. Please ask permission from azlyrics first before using 
	their lyrics. Apart from that you can use modify this app for other personal use."""


class MyLyrics(App):
	#------build method-------
	#	The purpose of the build function is to create the Layout and add the widgets as well.
	#	For this project I am using BoxLayout with Vertical Oreintation 
	# 
	def build(self):
		self.layout = BoxLayout(orientation='vertical')	
		self.layout.add_widget(Label(text='Please enter the song title',font_size='20sp',size_hint=(1, .2)))
		self.song_title_input = TextInput(text="",multiline=False,size_hint=(1, .2))
		self.layout.add_widget(self.song_title_input)
		self.layout.add_widget(Label(text='Please enter the song artist',font_size='20sp',size_hint=(1, .2)))
		self.song_artist_input = TextInput(text="",multiline=False,size_hint=(1, .2))
		self.layout.add_widget(self.song_artist_input)
		self.search = Button(text="Search Song",size_hint=(1, .2))
		self.search.bind(on_press=self.result)
		self.layout.add_widget(self.search)
		return self.layout

	#-----result methodd-----
	#	This method will crawl the lyrics from the azlyrics website and remove the html tags from it using beautiful soup.
	# 	and also to take spaces out of the song tile and song artist if there is any.
	def result(self,instance):
		odd_words = ["</br>","<br>","<div>","</div>","<i>","</i>"]
		song_artist = str(self.song_artist_input.text).replace(" ","")
		song_title = str(self.song_title_input.text).replace(" ","")
		# print (sa,st)
		url = 'http://www.azlyrics.com/lyrics/' + str(song_artist) +'/' + str(song_title) + '.html'

		#this error handling is important here becuase erros like Http 404 error can occur when the user enters non-existing
		# artist and song title and that will make your app not function well.Its always good to check for errors
		# even if it passes all tests.

		try:
			soup = BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")
			raw_lyrics_html = soup.find_all("div")
			lyrics = (str(raw_lyrics_html[22]))
			
			#this for loop will replace all html tags in the odd_word varaible with empty string.
			for word in odd_words:
				lyrics = lyrics.replace(str(word),"")

			intro ="This lyrics is brought to you by 'azlyrics.com' Enjoy"
			
			self.song_result = TextInput(text = intro + "\n" + lyrics, multiline = True, height = 70, size_hint = (1, 1))
			self.layout.add_widget(self.song_result)
			self.clearResult =Button(text = "Clear Lyrics",size_hint = (1, 0.2))
			self.clearResult.bind(on_press = self.removeWidget)
			self.layout.add_widget(self.clearResult)

		except Exception:
			self.song_result = TextInput(text = "There was no result for your search.\nPlease check spelling",\
						     multiline = True,height = 70,size_hint = (1, 1))
			self.layout.add_widget(self.song_result)
			self.clearResult = Button(text = "Clear Lyrics",size_hint = (1, 0.2))
			self.clearResult.bind(on_press = self.removeWidget)
			self.layout.add_widget(self.clearResult)

	#this method will remove the clear button and the previous lyrics from 
	# the app after before a new result(lyrics) arrive.
	def remove_Widget(self,instance):
		self.layout.remove_widget(self.song_result)
		self.layout.remove_widget(self.clearResult)


if __name__ == '__main__':
    MyLyrics().run()
