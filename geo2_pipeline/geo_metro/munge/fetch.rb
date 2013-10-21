require 'cgi'
require 'rubygems'
require 'json'
for line in STDIN
  q = CGI.escape(line.strip)
  url = "http://ws.geonames.org/searchJSON?maxRows=1&q=#{q}"
  json = %x[curl '#{url}'].strip
  raise if json =~ /\t/
  d = JSON.parse json
  x = d['geonames'][0]
  puts x.to_json
end
