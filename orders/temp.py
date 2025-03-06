from esewa.signature import generate_signature 

print(generate_signature("7",'40f3a66b-af54-4b1d-ad8e-766cbca91199'))
print(generate_signature("7.0",'40f3a66b-af54-4b1d-ad8e-766cbca91199'))
print(generate_signature("7.00000000",'40f3a66b-af54-4b1d-ad8e-766cbca91199'))