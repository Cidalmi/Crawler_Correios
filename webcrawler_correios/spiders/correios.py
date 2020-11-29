import scrapy
import bson

PAGE_LIMIT = 50
UFS = ['AL','AM','AP','BA','CE','DF','ES','GO','MA','MG','MS','MT','PA','PB','PE','PI','PR','RJ','RN','RO','RR','RS','SC','SE','SP','TO']
URL = "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm"


class CorreiosSpider(scrapy.Spider):
    name = 'correios'

    def start_requests(self):
        for uf in UFS:                        
            payload={'UF': uf, 'Localidade': '', 'qtdrow': str(PAGE_LIMIT), 'pagini': '1', 'pagfim': str(PAGE_LIMIT)}                
            yield scrapy.FormRequest(URL, callback=self.parse, method='POST', dont_filter=True, formdata=payload, meta={"lrecord":PAGE_LIMIT, "uf":uf})            
        
    def parse(self, response):                                
        result = response.xpath('//table[@class="tmptabela"][last()]//tr')        
        
        for result_und in result[1:]:            
            localidade = result_und.css('tr td:nth-child(1)::text').extract_first()        
            cep = result_und.xpath('td[2]//text()').extract_first()            
            if cep is not None or localidade is not None:                
                key = f"{localidade}:{cep}"
                yield {
                    'id': str(bson.ObjectId()),
                    'key': key,
                    'localidade': localidade,
                    'cep': cep
                } 
                
        next_page = response.xpath("//div [contains(@style,'float:left')] /a/text()").extract()                     
        
        if '[ Próxima ]' in next_page:                        
            lrecord = response.meta.get("lrecord")
            uf = response.meta.get("uf")          
            pagefim = lrecord+PAGE_LIMIT
            payload={'UF': uf, 'Localidade': '', 'qtdrow': str(PAGE_LIMIT), 'pagini': str(lrecord+1), 'pagfim': str(pagefim) }            
            yield scrapy.FormRequest(URL, callback=self.parse, method='POST', formdata=payload, dont_filter=True, meta={"lrecord": pagefim, "uf":uf})       
   

