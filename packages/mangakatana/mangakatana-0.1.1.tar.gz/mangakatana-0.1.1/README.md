[![Downloads](https://pepy.tech/badge/mangakatana)](https://pepy.tech/project/mangakatana) [![Downloads](https://pepy.tech/badge/mangakatana/month)](https://pepy.tech/project/mangakatana/month) [![Downloads](https://pepy.tech/badge/mangakatana/week)](https://pepy.tech/project/mangakatana/week)

# Mangakatana

```python
import mangakatana as mankat

result = mankat.search(title="Naruto")

second = result[1]

print(second.title, second.url, second.status)

for chapter in second.chapter_list():
	print(chapter.title, chapter.url)
```