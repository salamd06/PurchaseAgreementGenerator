from flask import Flask, render_template, request
import pdfFiller
from datetime import datetime

app = Flask(__name__)

def formatNumber(number):
    return f'{number:,}'
def formatDate(dateString):
    formatted_date = datetime.strptime(dateString, '%Y-%m-%d').strftime('%m-%d-%Y')
    return formatted_date

@app.route('/')
def index():
    return render_template('sampleFlask.html')

@app.route('/form', methods=["POST"])
def form():
    # print(request.form)
    buyer1 = request.form.get('buyer1Name')
    buyer1Email = request.form.get('buyer1Email')
    buyer1Phone = request.form.get('buyer1Phone')
    buyer2 = request.form.get('buyer2Name')
    buyer2Email = request.form.get('buyer2Email')
    buyer2Phone = request.form.get('buyer2Phone')
    mlsId = ''
    propertyAddress = request.form.get('propertyAddress')
    propertyCity = request.form.get('propertyCity')
    propertyState = request.form.get('propertyState')
    propertyZipCode = str(request.form.get('propertyZip'))
    propertyYearBuilt = str(request.form.get('propertyYearBuilt'))
    propertyLegalDescription = request.form.get('propertyLegalDescription')
    propertyCounty = request.form.get('propertyCounty')
    isThereAWell = True if request.form.get('toggleWellSeptic') == 'Yes' else False # need to add a check here for which thing is selected
    isThereaSepticSystem = True if request.form.get('toggleWellSeptic') == 'Yes' else False 
    wellAndSepticContingency = True if request.form.get('toggleWellContingency') == 'Yes' else False 
    wellAndSepticInspection = request.form.get('toggleWellAndSepticInspectionRequired') # Well, Septic, Both or No
    wellAndSepticInspectionTimePeriod = str(request.form.get('inspectionPeriodDays')) # days
    whoPaysForWellAndSepticInspection = request.form.get('wellAndSepticInspectionPaidBy') # Buyer or Seller

    cityWaterAndSewerToggle = request.form.get('toggleCityWaterSewer') # options are City Water only, City sewer only, both or neither
    if cityWaterAndSewerToggle == "City Water only":
        cityWater = True
        citySewer = False
    elif cityWaterAndSewerToggle == "City Sewer only":
        cityWater = False
        citySewer = True
    elif cityWaterAndSewerToggle == "Both":
        cityWater = True
        citySewer = True
    elif cityWaterAndSewerToggle == "Neither":
        cityWater = False
        citySewer = False
    homeWarrantyAddedToPA = True if request.form.get('toggleHomeWarranty') == 'Yes' else False
    homeWarrantyObtainedBy = request.form.get('homeWarrantyObtainedBy')
    homeWarrantyPaidForBy = request.form.get('homeWarrantyPaidBy')
    homeWarrantyCompanyName = request.form.get('homeWarrantyCompany')
    homeWarrantyUpToAmount = str(request.form.get('homeWarrantyAmount'))
    isSellerForeignPerson = True if request.form.get('isSellerAForeignPerson') == 'Yes' else False
    purchasePrice = formatNumber(request.form.get('purchasePrice'))
    ifBuyerCannotcloseEarnestMoneyWillBeGivenTo = request.form.get('writtenStatementEarnestMoney')
    contingentOnInspection = True if request.form.get('toggleContingentOnInspection') == 'Yes' else False
    buyerElectsInspection = 'Yes' if contingentOnInspection == 'Yes' else request.form.get('toggleGetInspection')
    earnestMoney = formatNumber(request.form.get('earnestMoney'))
    closeDate = formatDate(request.form.get('closeDate'))
    inspectionPeriod = str(request.form.get('inspectionPeriod'))
    toggleSellerContribution = True if request.form.get('toggleSellerContribution') == 'Yes' else False
    sellerContributionType = request.form.get('sellerContributionType') #dollars or percentage
    sellerContributionAmount = formatNumber(request.form.get('sellerContributionAmount'))
    writtenStatementRequired = True if request.form.get('toggleWrittenStatement') == 'Yes' else False
    contingentOnBuyerProperty = True if request.form.get('contingentOnBuyersProperty') == 'Yes' else False  # This should be a boolean value, true or false
    contingentOnBuyerHasPurchaseAgreement = True if request.form.get('togglePurchaseAgreementOnContingentHome') == 'Yes' else False  # This should be a boolean value, true or false
    if contingentOnBuyerProperty:
        if contingentOnBuyerHasPurchaseAgreement:
            contingentOnBuyerPropertyOption = '2'
        else:
            contingentOnBuyerPropertyOption = '1'
    else:
        contingentOnBuyerPropertyOption = '3'
    contingentOnBuyerPropertyAddress = request.form.get('inputContingentAddress')
    contingentOnBuyerPropertyCity = request.form.get('inputContingentCity')
    contingentOnBuyerPropertyState = request.form.get('inputContingentState')
    contingentOnBuyerPropertyZip = request.form.get('inputContingentZip')
    contingentOnBuyerPropertyClosingDate = formatDate(request.form.get('scheduledCloseDateOnContingentHome'))
    proratedTaxes = True
    sellerPaidHomesteadDifference = True
    possession = 'At Closing'
    # not yet in form
    sellerDisclosureReceived = 'Property Disclosure Statement' # second option would be disclosure alternatives, third would be none
    # not yet in form
    financingType = request.form.get('financingType') # This will be either 'Conventional', 'FHA', 'VA', 'DVA', 'USDA', or '100% Cash'
    downPaymentPercentage = '100' if financingType == '100% Cash' else str(request.form.get('downPaymentPercentage'))
    mortgageFinancingPercentage = str(100-int(downPaymentPercentage))
    secondaryFinancing = True if request.form.get('toggleSecondMortgage') == 'Yes' else False
    writtenStatementDate = formatDate(request.form.get('writtenStatementDate'))
    contingentOnFinancing = True if request.form.get('toggleFinanceContingency') == 'Yes' else False
    sellerPaidLenderProcessingFees = True if request.form.get('sellerPaidLenderProcessingFee') == 'Yes' else False
    vaFundingFeeAmount = formatNumber(request.form.get('vaFundingFee'))
    vaFundingFeePaidBy = request.form.get('vaFundingFeePaidBy')
    vaFundingFeeAddedWhere = request.form.get('vaFundingFeeAddedWhere')
    maxInterestRate = str(request.form.get('maxInterestRate'))
    listingAgentName = request.form.get('listingAgentName') #
    listingAgentCompany = request.form.get('listingAgentCompany') #
    listingAgentEmail = request.form.get('listingAgentEmail') #
    listingAgentPhone = request.form.get('listingAgentPhone')#
    buyerAgentName = request.form.get('buyerAgentName')
    buyerAgentCompany = request.form.get('buyerAgentCompany')
    buyerAgentEmail = request.form.get('buyerAgentEmail')
    buyerAgentPhone = request.form.get('buyerAgentPhone')
    buyerAgentAgencyType = request.form.get('buyerAgentAgencyType')
    listingAgentAgencyType = "Dual Agent" if request.form.get('buyerAgentAgencyType') == "Dual Agent" or listingAgentCompany == buyerAgentCompany else "Seller's Agent"
    buyerAgentCommissionType = request.form.get('buyerAgentCommissionType')  # This will identify percentage or dollars
    buyerAgentCommission = str(request.form.get('buyerAgentCommission'))

    # need to add year built to see if we need lead based paint addendum
    # need to add septic and well inspection contingency addendum
    paFormData = {
        "Buyer Information": {
            "Buyer 1": buyer1,
            "Buyer 1 Email": buyer1Email,
            "Buyer 1 Phone": buyer1Phone,
            "Buyer 2": buyer2,
            "Buyer 2 Email": buyer2Email,
            "Buyer 2 Phone": buyer2Phone,
            },
        "Property Information": {
            "MLS ID": "",
            "Street Address": propertyAddress,
            "City": propertyCity, 
            "State": propertyState,  
            "County": propertyCounty,
            "Zip Code": propertyZipCode,
            "Year Built": propertyYearBuilt,
            "Legal Description": propertyLegalDescription, 
            "Well and Septic": {
                "Well": isThereAWell, #True/False
                "Septic": isThereaSepticSystem, #True/False
                "Contingency": wellAndSepticContingency, #True/False
                "Who Pays for Inspection": whoPaysForWellAndSepticInspection, #Buyer or Seller
                "Inspection Time Period": wellAndSepticInspectionTimePeriod, #in days
                "Inspection Scope": wellAndSepticInspection, #Well, Septic, Both or None
                },
            "City Water": cityWater, #True/False
            "City Sewer": citySewer, #True/False
            "Home Warranty": {
                "Added to PA": homeWarrantyAddedToPA, #True/False
                "To Be Obtained By": homeWarrantyObtainedBy,
                "Paid For By": homeWarrantyPaidForBy,
                "Company Name": homeWarrantyCompanyName,
                "Up To Amount": homeWarrantyUpToAmount
                },
            "Is Seller Foreign Person": isSellerForeignPerson, #True/False
            # "HOA Information": {
            #     "HOA Exists": False,  # True/False
            #     "HOA Name": 'Gassen',
            #     "HOA Address": "",
            #     "HOA Phone": "",
            #     "Monthly Dues": "",
            #     "Special Assessments": "",
                # }
            },
        "Offer Information": {
            "Purchase Price": purchasePrice,
            "Earnest Money": earnestMoney,
            "Close Date": closeDate,
            "Inspection Details":{
                "Contingent on Inspection": contingentOnInspection, #True/False
                "Buyer Elects to Have An Inspection": buyerElectsInspection, #True/False
                "Inspection Period": inspectionPeriod,
                },
            "Seller Contribution": {
                "Seller is Contributing": toggleSellerContribution, # True/false
                "Seller Contribution Type": sellerContributionType, #$ or %
                "Seller Contribution Amount": sellerContributionAmount, #should be a number
                },
            "Sale of Buyer Property Contingency": {
                "Option": contingentOnBuyerPropertyOption, #1: subject to addendum Sale of Buyer's Property Contingency(for sale or not listed yet), 2: home is scheduled to close, 3: not contingent
                "Is Currently Listed": True,
                "Number of Days to be Listed": '7',
                "Broker to be Listed With": 'LPT Realty',
                "numberOfDaysToRemoveContingencyIfSellerDemands": '7',
                "Property Address": contingentOnBuyerPropertyAddress,
                "Property City": contingentOnBuyerPropertyCity,
                "Property State": contingentOnBuyerPropertyState,
                "Property Zip": contingentOnBuyerPropertyZip,
                "Closing Date": contingentOnBuyerPropertyClosingDate,
                },
            "Lead Based Paint Addendum": {
                "Required": False,  # This should be set to True if the year built is before 1978
                "Buyer Elects to Have Inspection": False,  # True/False, if the buyer elects to have an inspection for lead-based paint
                "Inspection Period": "",  # This should be the number of days for the inspection period if required
                },
            "Taxes": {
                "Prorated": proratedTaxes,
                "Seller Paid Homestead Difference": sellerPaidHomesteadDifference
                },
            "Possession": possession,
            "Seller Disclosure Received by Buyer": sellerDisclosureReceived,
            'otherContingenciesSection':''
            },
        "Financing": {
            "financingType": financingType,
            "downPaymentPercentage": downPaymentPercentage,
            "mortgageFinancingPercentage": mortgageFinancingPercentage,
            "assumingFinancingPercentage": "",
            "contractForDeedPercentage": "",
            "secondaryFinancing": secondaryFinancing, # True/false
            "writtenStatement": {
                'required': writtenStatementRequired,  # True/false
                'date': writtenStatementDate,  # Date of the written statement
                },
            "contingentOnFinancing": contingentOnFinancing, # True/false
            "sellerPaidLenderProcessingFees": sellerPaidLenderProcessingFees, #va and fha only
            "vaFundingFee": {
                "amount": vaFundingFeeAmount,
                "paidBy": vaFundingFeePaidBy,
                "addedWhere": vaFundingFeeAddedWhere
                },
            "maxInterestRate": maxInterestRate,
            "ifBuyerCannotCloseEarnestMoneyWillBeGivenTo": ifBuyerCannotcloseEarnestMoneyWillBeGivenTo,
            },
        "Agency": {
            "Listing Agent Name": listingAgentName,
            "Listing Agent Company": listingAgentCompany,
            "Listing Agent Email": listingAgentEmail,
            "Listing Agent Phone": listingAgentPhone,
            "Listing Agent Agency Type": listingAgentAgencyType,
            "Buyer Agent Name": buyerAgentName,
            "Buyer Agent Company": buyerAgentCompany,
            "Buyer Agent Email": buyerAgentEmail,
            "Buyer Agent Phone": buyerAgentPhone,
            "Buyer Agent Agency Type": buyerAgentAgencyType,
            "Buyer Agent Commission Type": buyerAgentCommissionType,
            "Buyer Agent Commission": buyerAgentCommission,
            },
        }
    print(paFormData)
    pdfFiller.fillPurchaseAgreement(paFormData)

    return render_template('sampleFlaskFormSubmission.html')
    # return render_template(r'C:\Users\salam\Desktop\Desktop Items\Code\Real Estate\templates\sampleFlask.html')
    # return

# app.run(host = '0.0.0.0.', port=80)

if __name__ == '__main__':
    app.run(debug=False) #must be set to false in production environment