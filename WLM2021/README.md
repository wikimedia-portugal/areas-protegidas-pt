# WLM 2021 table conversion

These are instructions to convert the Listeria-generated tables
into cleaned-up and simplified tables
that can be used in the wikilovesmonuments.org.pt.

## Getting the content

- Open one of the pages, e.g. <https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:Wiki_Loves_Monuments_2019/Portugal/Lista/Aveiro>
- Use the browser's functionality to view the page source
  <details><summary>Side note: Why use "view source" rather than "inspect"</summary>
  View source is preferred to using the inspector tool,
  since that includes javascript modifications to the DOM
  and additional changes, namely:

  - table header has javascript-added attributes, mostly for sorting
  - map links are replaced by javascript links (though neither is usable from a third-party website)
  - images have width and height attributes moved to the end of the element
  - br and img tags are unclosed
  </details>
- Copy the html of the table and paste into a new file
- Apply the regex replacements listed in the following section, in order.

## Replacements

- Remove line breaks before `</td>` closing tags:<br/>
  `s┃\n(</t[dh])┃$1┃`

- Add line breaks before `</tr>` closing tags:<br/>
  `s┃></tr┃>\n</tr┃`

- Remove the `<tbody>` tag:<br/>
  `s┃</?tbody>┃┃`

- Indent the `<td>` and `<th>` tags:<br/>
  `s┃^(<t[dh])┃    $1┃`

- Remove unnecessary attributes:<br/>
  `s┃ (style|class|rel|title|data-[\w-]+)="[^"]+"┃┃`

- Remove unnecessary columns, and reorder the remaining ones:<br/>
  `s┃(<tr>\n +<t[dh].+)(\n +<t[dh].+)\n +<t[dh].+(\n +<t[dh].+)\n +<t[dh].+(\n +<t[dh].+)\n +<t[dh].+(\n +<t[dh].+)\n +<t[dh].+(\n +<t[dh].+)┃$1$3$2$4$5$6┃`

- Replace the `<br>` tags in the SIPA/DGPC column with spaces:<br/>
  `s┃<br/>┃ ┃`

- Add the domain to ptwiki links:<br/>
  `s┃href="/w┃href="https://pt.wikipedia.org/w┃`

- Remove text content of Wikidata links, and add tooltip:<br/>
  `s┃<a (href=".+")>(Q\d+)</a>┃<a title="Item no Wikidata: $2" $1></a>┃`

- Remove text content of map links, add tooltip, and rewrite URL to point to OSM:<br/>
  `s┃<a href="https?://pt.wikipedia.org/wiki/Especial:Map/(\d+)/([\d.-]+)/([\d.-]+)/pt">.+</a>┃<a title="Localização no mapa" href="https://www.openstreetmap.org/?mlat=$2&amp;mlon=$3&amp;zoom=$1"></a>┃`

- Remove images from "upload" column (they're added via CSS):<br/>
  `┃(<a href="https://commons.+?">)<img.+/></a>┃$1</a>┃`
