# xpe

*Finally, a commandline xpath tool for linux that doesn't suck.*

***What is this?***

xpe is a commandline xpath parser. Pipe in some textual data, supply it with an xpath expression, and it will dump the result to stdout. Perfect for shellscripting. For example:

    
    curl -sL github.com | xpe "//meta[@name='twitter:title']"

    GitHub: Where the world builds software
    
