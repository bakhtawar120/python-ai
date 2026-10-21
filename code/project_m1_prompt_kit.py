
business_name = input("Business name: ")
business_type = input("Business type: ")
city = input("City: ")
customers = input("Main customers: ")
# Why comment 1: input() hamesha text deta hai, isliye budget ko int() mein convert kiya
budget = int(input("Monthly budget (PKR): "))

# Why comment 2: header mein business ka naam taake output client ko personal lage
print("\n=========================================")
print(f"   AI Prompt Kit for {business_name}")
print("=========================================")

# Why comment 3: har prompt mein role, task, audience aur tone rakha taake AI ka jawab specific aaye
print("\n[1] Marketing")
print(f"Write a short Instagram post for {business_name}, a {business_type} in {city}. ...")

print("\n[2] Customer Service")
print(f"You are the manager of {business_name}. Write a polite reply ... ")

print("\n[3] Growth")
print(f"Suggest 3 low-cost AI tools a {business_type} in {city} can use ... {budget} PKR per month.")


