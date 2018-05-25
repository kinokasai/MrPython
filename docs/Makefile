report:
		bash include_md.sh report.md > full_report.md;\
		./side_code.sh full_report.md;\
		pandoc -t json out.md | python ./tex_templates/underline.py | \
		pandoc -f json -o report.pdf --pdf-engine=xelatex --toc \
		--template=tex_templates/template.latex &&\
		echo "Done."