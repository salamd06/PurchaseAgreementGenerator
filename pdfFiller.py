from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from datetime import datetime
import re
from num2words import num2words

pdfPaths={
    'Blank Purchase Agreement': 'C:\\Users\\salam\\Desktop\\Desktop Items\\Code\\Real Estate\\re forms\\Purchase Agreement (08_2024).pdf',
    'Blank Sale of Buyer Property Contingency Addendum': 'C:\\Users\\salam\\Desktop\\Desktop Items\\Code\\Real Estate\\re forms\\Addendum to PA - Sale of Buyers Property Contingency(Rev. 08_2021).pdf',
    'Blank Well and Septic Contingency Addendum': 'C:\\Users\\salam\\Desktop\\Desktop Items\\Code\\Real Estate\\re forms\\Addendum to PA - Septic and Well Inspection Contingency (Rev. 08_2022).pdf',
    'Blank Lead Based Paint Addendum': 'C:\\Users\\salam\\Desktop\\Desktop Items\\Code\\Real Estate\\re forms\\Addendum to PA Lead-Based Paint.pdf',
}

def fillInDateAndProperty(can, date, address):
    can.drawString(425, 732, date)
    can.drawString(160, 715, address)
    return

def createSaleOfBuyerPropertyContingencyAddendum(options):
    existingSaleOfBuyerPropertyPdf = PdfReader(pdfPaths['Blank Sale of Buyer Property Contingency Addendum'])
    packet1 = BytesIO()
    page1 = existingSaleOfBuyerPropertyPdf.pages[0]
    c = canvas.Canvas(packet1, pagesize=letter)
    c.drawString(425, 673, options['today'])  # Date at the top right corner
    c.drawString(380, 643, options['today'])  # Date of PA
    c.drawString(64, 616, options['address']) #address of property you are making an offer on
    c.drawString(190, 589, options['contingentAddress']) #address of property you are making an offer on
    if options['isCurrentlyListed']:
        c.drawString(150, 569, 'X') #Is Currently Listed
    else:
        c.drawString(269, 569, 'X') #to Be listed within checkbox
        c.drawString(440, 573, options['numberOfDaysToBeListed']) #to be listed within X number of days
    c.drawString(64, 546, options['brokerListedWith']) #brokerListedWith
    c.drawString(495, 452, options['numberOfDaysToRemoveContingencyIfSellerDemands']) #days to remove contingency if seller demands

    c.save()
    packet1.seek(0)
    newPdf = PdfReader(packet1)
    page1.merge_page(newPdf.pages[0])
    return page1

def createWellAndSepticContingencyAddendum(options, address): #returns an array of pages which then need to be added to the output pdf
    today = datetime.today().strftime("%m/%d/%Y")
    existingPdf = PdfReader(pdfPaths['Blank Well and Septic Contingency Addendum'])
    fullAddress = address
    listOfPages = []

    for pageNumber in range(len(existingPdf.pages)):
        p = existingPdf.pages[pageNumber]
        packet2 = BytesIO()
        c = canvas.Canvas(packet2, pagesize=letter)
        if pageNumber == 0:
            #page "0" is page 1
            c.drawString(385, 660, today)
            c.drawString(370, 632, today)
            c.drawString(64, 600, fullAddress)
            if options['Inspection Scope'] == 'Septic' or options['Inspection Scope'] == 'Both':
                c.drawString(64, 440, 'X') #septic system contingency applies
                c.drawString(444, 432, options['Inspection Time Period']) #septic inspection period in days
            if options['Who Pays for Inspection'] == 'Buyer':
                c.drawString(82, 398, 'X') #buyer agrees to pay for septic inspection
            else:
                c.drawString(135, 398, 'X') #seller agrees to pay for septic inspection
        elif pageNumber == 1:
            c.drawString(164, 671, fullAddress)
            if options['Inspection Scope'] == 'Well' or options['Inspection Scope'] == 'Both':
                c.drawString(64, 643, 'X') #well contingency applies
                c.drawString(444, 635, options['Inspection Time Period']) #well inspection period in days
            if options['Who Pays for Inspection'] == 'Buyer':
                c.drawString(82, 601, 'X') #buyer agrees to pay for well inspection
            else:
                c.drawString(135, 601, 'X') #seller agrees to pay for well inspection
   
        c.save()
        packet2.seek(0)
        newPdf2 = PdfReader(packet2)
        p.merge_page(newPdf2.pages[0])
        # output.add_page(p)
        listOfPages.append(p)
    return listOfPages

def createLeadBasedPaintContingencyAddendum(options, address): #returns an array of pages which then need to be added to the output pdf
    today = datetime.today().strftime("%m/%d/%Y")
    existingPdf = PdfReader(pdfPaths['Blank Lead Based Paint Addendum'])
    fullAddress = address
    listOfPages = []

    for pageNumber in range(len(existingPdf.pages)):
        p = existingPdf.pages[pageNumber]
        packet2 = BytesIO()
        c = canvas.Canvas(packet2, pagesize=letter)
        if pageNumber == 0:
            c.drawString(385, 660, today)
            c.drawString(370, 632, today)
            c.drawString(64, 600, fullAddress)
            if options['Buyer Elects to Have Inspection']:
                c.drawString(64, 156, 'X') # Buyer Elects to Have An Inspection
                if options['Inspection Period'] == '10':
                    c.drawString(200, 96, 'X') #10 day inspection period
                else:
                    c.drawString(259, 96, 'X') #x days inspection period checkbox
                    c.drawString(288, 99, options['Inspection Period']) #inspection period in days
            else:
                c.drawString(64, 188, 'X') # Buyer Waives Inspection

        elif pageNumber == 1:
            c.drawString(164, 671, fullAddress)
   
        c.save()
        packet2.seek(0)
        newPdf2 = PdfReader(packet2)
        p.merge_page(newPdf2.pages[0])
        listOfPages.append(p)
    return listOfPages

def testNewPdf(offerData, testPdfPath):
    filled_pdf_path = f'C:\\Users\\salam\\Desktop\\Desktop Items\\Code\\Real Estate\\re forms\\test.pdf'
    today = datetime.today().strftime("%m/%d/%Y")
    existingPdf = PdfReader(testPdfPath)
    output = PdfWriter()
    fullAddress = '1331 ashton ct, chanhassen, mn 55317'

    for pageNumber in range(len(existingPdf.pages)):
        page = existingPdf.pages[pageNumber]
        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)
        if pageNumber == 0:
            c.drawString(385, 660, today)
            c.drawString(370, 632, today)
            c.drawString(64, 600, fullAddress)
            c.drawString(64, 188, 'X') # Buyer Waives Inspection
            c.drawString(64, 156, 'X') # Buyer Elects to Have An Inspection

            c.drawString(200, 96, 'X') #10 day inspection period
            c.drawString(259, 96, 'X') #x days inspection period
            c.drawString(288, 99, '7') #septic inspection period in days
        elif pageNumber == 1:
            c.drawString(164, 671, fullAddress)
   
        c.save()
        packet.seek(0)
        try:
            newPdf = PdfReader(packet)
            page.merge_page(newPdf.pages[0]) # Merge the Sale of Buyer Property Contingency Addendum if it exists
        except IndexError:
            print(f'No content added to page number {pageNumber+1}')
        output.add_page(page)

    with open(filled_pdf_path, 'wb') as output_stream:
        output.write(output_stream)
    return

def fillPurchaseAgreement(offerData):
    savePath = f'C:\\Users\\salam\\Desktop\\Desktop Items\\Code\\Real Estate\\re forms\\Filled_Purchase_Agreement.pdf'
    # savePath = f'C:\\Users\\salam\\Desktop\\Desktop Items\\Code\\Real Estate\\re forms\\PA for {offerData['Property Information']["Street Address"]}_{offerData['Property Information']['City']}.pdf'

    today = datetime.today().strftime("%m/%d/%Y")
    existingPdf = PdfReader(pdfPaths['Blank Purchase Agreement'])
    output = PdfWriter()

    fullAddress = f'{offerData['Property Information']["Street Address"]}, {offerData['Property Information']["City"]}, {offerData['Property Information']["State"]} {offerData['Property Information']["Zip Code"]}'
    saleOfBuyerPropertyContingencyAddendumPdf = None
    wellAndSepticContingencyAddendum = None
    leadBasedPaintContingencyAddendum = None

    for pageNumber in range(len(existingPdf.pages)):
        page = existingPdf.pages[pageNumber]
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        if pageNumber == 0:
            #page "0" is page 1
            can.drawString(385, 705, today)
            can.drawString(120, 675, offerData['Buyer Information']['Buyer 1'])
            if offerData['Buyer Information']['Buyer 2'] != '':
                can.drawString(120, 660, offerData['Buyer Information']['Buyer 2'])
            can.drawString(415, 628, offerData['Offer Information']['Earnest Money']) 
            earnestMoneyInt = int(offerData['Offer Information']['Earnest Money'].replace(',',''))
            can.drawString(64, 628, numberToText(earnestMoneyInt))
            can.drawString(145, 535, offerData['Property Information']['Street Address'])
            can.drawString(100, 520, offerData['Property Information']['City'])
            can.drawString(385, 520, offerData['Property Information']['County'])
            can.drawString(195, 505, offerData['Property Information']['Zip Code'])
            can.drawString(80, 488, offerData['Property Information']['Legal Description'])
            can.drawString(350, 193, offerData['Offer Information']['Purchase Price'])
            purchasePriceInt = int(offerData['Offer Information']['Purchase Price'].replace(',',''))
            can.drawString(64, 177, numberToText(purchasePriceInt)) #purchase price text
            can.drawString(200, 45, offerData['Offer Information']['Close Date'])
            can.drawString(95, 150, offerData['Financing']['downPaymentPercentage'])
            can.drawString(95, 134, offerData['Financing']['mortgageFinancingPercentage'])
            can.drawString(95, 118, offerData['Financing']['assumingFinancingPercentage'])
            can.drawString(95, 90, offerData['Financing']['contractForDeedPercentage'])
        elif pageNumber == 1:
            fillInDateAndProperty(can, today, fullAddress)
            if offerData['Financing']['contingentOnFinancing']: #this shows true if you click a mortgage but go back to 100% cash
                can.drawString(183, 670, 'X')
                can.drawString(70, 480, '30') # need to fix this
                can.drawString(370, 480, offerData['Financing']['maxInterestRate'])
            else:
                can.drawString(210, 670, 'X')
            if offerData['Financing']['financingType'] == 'Conventional':
                can.drawString(64, 572, 'X')
            elif offerData['Financing']['financingType'] == 'VA':
                can.drawString(64, 558, 'X')
            elif offerData['Financing']['financingType'] == 'FHA':
                can.drawString(64, 544, 'X')
            elif offerData['Financing']['financingType'] == 'USDA':
                can.drawString(64, 530, 'X')
            if offerData['Financing']['secondaryFinancing']:
                can.drawString(195, 604, 'X')
            else:
                can.drawString(64, 604, 'X')
            if offerData['Financing']['writtenStatement']['required']:
                can.drawString(64, 286, 'X')
                can.drawString(140, 271, offerData['Financing']['writtenStatement']['date'])
            elif offerData['Financing']['ifBuyerCannotCloseEarnestMoneyWillBeGivenTo'] == 'Buyer':
                can.drawString(82, 353, 'X')
            elif offerData['Financing']['ifBuyerCannotCloseEarnestMoneyWillBeGivenTo'] == 'Seller':
                can.drawString(209, 353, 'X')     
        elif pageNumber == 2:
            fillInDateAndProperty(can, today, fullAddress)
            if offerData['Financing']['writtenStatement']['required']:
                if offerData['Financing']['ifBuyerCannotCloseEarnestMoneyWillBeGivenTo'] == 'Buyer':
                    can.drawString(400, 486, 'X')
                    can.drawString(310, 430, 'X')
                elif offerData['Financing']['ifBuyerCannotCloseEarnestMoneyWillBeGivenTo'] == 'Seller':
                    can.drawString(276, 486, 'X')
                    can.drawString(186, 430, 'X')
            # if offerData['Financing']['financingType'] != '100% Cash':
            if offerData['Financing']['contingentOnFinancing']:
                can.drawString(64, 357, 'X') #Buyer can lock in the interest rate at any time prior to closing or as required by lender
                can.drawString(390, 336, '0') #Seller agrees to pay up to X to make repairs as required by the lender commitment
                can.drawString(123, 218, 'X') #Buyer agrees to pay any reinspection fee required by the Buyer's lender
            if offerData['Financing']['financingType'] == 'FHA':
                can.drawString(300, 125, offerData['Offer Information']['Purchase Price'])
        elif pageNumber == 3:
            fillInDateAndProperty(can, today, fullAddress)
            if offerData['Financing']['financingType'] == 'FHA':
                can.drawString(435, 675, offerData['Financing']['sellerPaidLenderProcessingFees'])
            if offerData['Financing']['financingType'] == 'VA':
                can.drawString(435, 675, offerData['Financing']['sellerPaidLenderProcessingFees'])
                if offerData['Financing']['vaFundingFee']['amount'] != '':
                    if offerData['Financing']['vaFundingFee']['paidBy'] == 'Buyer':
                        can.drawString(65, 613, offerData['Financing']['vaFundingFee']['amount'])
                        if offerData['Financing']['vaFundingFee']['addedWhere'] == 'At Closing':
                            can.drawString(318, 610, 'X')
                        else:
                            can.drawString(399, 610, 'X')
                    else:
                        can.drawString(65, 595, offerData['Financing']['vaFundingFee']['amount'])
            if offerData['Offer Information']['Seller Contribution']['Seller is Contributing']:
                can.drawString(92, 390, 'X') #Seller is contributing
                if offerData['Offer Information']['Seller Contribution']['Seller Contribution Type'] == '$':
                    can.drawString(64, 363, 'X') #Seller is contributing a fixed amount
                    can.drawString(90, 365, offerData['Offer Information']['Seller Contribution']['Seller Contribution Amount'])
                else: #Seller is contributing a percentage of the sale price
                    can.drawString(64, 345, 'X') #Seller is contributing a percentage of the purchase price
                    can.drawString(90, 347, offerData['Offer Information']['Seller Contribution']['Seller Contribution Amount'])
            else:
                can.drawString(116, 390, 'X') # Seller is not contributing
            if offerData['Offer Information']['Inspection Details']['Contingent on Inspection']:
                can.drawString(182, 178, 'X') #Contingent on inspection
            else:
                can.drawString(209, 178, 'X') #Not contingent on inspection
            if offerData['Offer Information']['Inspection Details']['Buyer Elects to Have An Inspection']:
                can.drawString(411, 212, 'X') #Elects Inspection
                can.drawString(138, 75, 'X') # seller does not allow buyer to perform intrustive testing or inspection
            else:
                can.drawString(469, 212, 'X') #Declines to have Inspection
        elif pageNumber == 4:
            fillInDateAndProperty(can, today, fullAddress)
            if offerData['Offer Information']['Inspection Details']['Buyer Elects to Have An Inspection']:
                can.drawString(110, 671, offerData['Offer Information']['Inspection Details']['Inspection Period'])
            if offerData['Offer Information']['Sale of Buyer Property Contingency']['Option'] == '1':
                can.drawString(64, 443, 'X') #Option 1
            if offerData['Offer Information']['Sale of Buyer Property Contingency']['Option'] == '2':
                can.drawString(64, 401, 'X') #Option 2
                contingentAddress = f'{offerData["Offer Information"]["Sale of Buyer Property Contingency"]["Property Address"]}, {offerData["Property Information"]["City"]}, {offerData["Property Information"]["State"]} {offerData["Property Information"]["Zip Code"]}'
                can.drawString(110, 387, contingentAddress) #Option 2
                can.drawString(110, 368, offerData['Offer Information']['Sale of Buyer Property Contingency']['Closing Date']) #Option 2

            if offerData['Offer Information']['Sale of Buyer Property Contingency']['Option'] == '3':
                can.drawString(64, 275, 'X') #Option 3

            if offerData['Offer Information']['Taxes']['Prorated']:
                can.drawString(134, 191, 'X')
                can.drawString(130, 153, 'X')
            if offerData['Offer Information']['Taxes']['Seller Paid Homestead Difference']:
                can.drawString(462, 115, 'X')
            else:
                can.drawString(510, 115, 'X')
        elif pageNumber == 5:
            fillInDateAndProperty(can, today, fullAddress)
            #Seller shall pay deferred taxes
            can.drawString(178, 675, 'X')
            can.drawString(441, 637, 'X')
            can.drawString(200, 586, 'X')
            can.drawString(198, 535, 'X')

            #Has Seller received notice of new improvements or assessments?
            can.drawString(435, 441, 'X') #has not
            # can.drawString(170, 540, 'X')
            #Previously executed purchase agreement?
            can.drawString(476, 288, 'X') #Is Not subject to cancellation of previously executed purchase agreement

            # Deed Type
            can.drawString(64, 178, 'X') #Warranty Deed
            # can.drawString(164, 178, 'X') #Personal Representative's Deed
            # can.drawString(360, 178, 'X') #Contract for Deed
            # can.drawString(481, 178, 'X') #Trustee's Deed
        elif pageNumber == 6:
            fillInDateAndProperty(can, today, fullAddress)
            if offerData['Offer Information']['Possession'] == 'At Closing':
                can.drawString(64,679, 'X') #Buyer to take possession At Closing
            else:
                can.drawString(64,661, 'X') #Buyer to take possession 'Other' Selection
                can.drawString(120,664, offerData['Offer Information']['Possession']) #Buyer to take possession 'Other' Selection
        elif pageNumber == 7:
            fillInDateAndProperty(can, today, fullAddress)
            if offerData['Offer Information']['Seller Disclosure Received by Buyer'] == 'Property Disclosure Statement':
                can.drawString(310,144, 'X') #Buyer received Seller's Property Disclosure Statement
            if offerData['Offer Information']['Seller Disclosure Received by Buyer'] == 'Disclosure Alternatives':
                can.drawString(216,130, 'X') #Buyer received Seller's Disclosure alternatives
        elif pageNumber == 8:
            fillInDateAndProperty(can, today, fullAddress)
            #Well and Septic
            if offerData['Property Information']['City Water']:
                can.drawString(273,653, 'X') #Property is hooked up to city Water
            else:
                can.drawString(309,653, 'X') #Property is Not hooked up to city Water
            if offerData['Property Information']['City Sewer']:
                can.drawString(128,654, 'X') #Property is hooked up to city Sewer
            else:
                can.drawString(167,654, 'X') #Property is Not hooked up to city Sewer
            if offerData['Property Information']['Well and Septic']['Well']:
                can.drawString(116,555, 'X') #Seller Knows Property has Well
            else:
                can.drawString(172,555, 'X') #Property has no Well
            if offerData['Property Information']['Well and Septic']['Septic']:
                can.drawString(108,620, 'X') #Seller Knows Property has Septic
            else:
                can.drawString(159,620, 'X') #Property has No Septic
            if offerData['Property Information']['Well and Septic']['Contingency']:
                can.drawString(210,516, 'X') #Add Well And Septic Contingency Addendum
            else:
                can.drawString(237,516, 'X') #Dont Add Well and Septic Contingency Addendum
            
            #Home Protection Warranty Plan
            #Home Warranty will be obtained
            if offerData['Property Information']['Home Warranty']['Added to PA']:
                can.drawString(64,370, 'X') #Home Warranty will be obtained
                if offerData['Property Information']['Home Warranty']['To Be Obtained By'] == 'Buyer':
                    can.drawString(364,370, 'X') #by Buyer
                else:
                    can.drawString(428,370, 'X') #by Seller
                if offerData['Property Information']['Home Warranty']['Paid For By'] == 'Buyer':
                    can.drawString(82,344, 'X') #Paid for by Buyer
                else:
                    can.drawString(137,344, 'X') #Paid for by Seller
                can.drawString(280,346, offerData['Property Information']['Home Warranty']['Company Name']) #Issued by (company name)
                can.drawString(200,320, offerData['Property Information']['Home Warranty']['Up To Amount']) #up to this amount
            else:
                can.drawString(64,299, 'X') #Home Warranty will NOT be obtained

            #Agency Notice
            if offerData['Agency']['Listing Agent Name'] != '':
                can.drawString(64,246, offerData['Agency']['Listing Agent Name']) #licensee 1
                if offerData['Agency']['Listing Agent Agency Type'] == 'Dual Agent':
                    can.drawString(446,243, 'X') #first line dual Agent
                if offerData['Agency']['Listing Agent Agency Type'] == "Seller's Agent":
                    can.drawString(281,243, 'X') #first line seller's Agent
            if offerData['Agency']['Listing Agent Company'] != '':
                can.drawString(64,218, offerData['Agency']['Listing Agent Company']) #licensee 1 broker
            if offerData['Agency']['Buyer Agent Name'] != '':
                can.drawString(64,190, offerData['Agency']['Buyer Agent Name']) #licensee 2
                if offerData['Agency']['Buyer Agent Agency Type'] == "Buyer's Agent":
                    can.drawString(362,187, 'X') #second line buyer's agent
                if offerData['Agency']['Buyer Agent Agency Type'] == 'Dual Agent':
                    can.drawString(446,187, 'X') #second line dual Agent
                if offerData['Agency']['Buyer Agent Company'] != '':
                    can.drawString(64,162, offerData['Agency']['Buyer Agent Company']) #licensee 2 broker
                if offerData['Agency']['Buyer Agent Commission Type'] != '%':
                    can.drawString(415,88, offerData['Agency']['Buyer Agent Commission']) #Seller's Contribution to Buyer's Broker Compensation in dollars, one or the other
                else:
                    can.drawString(195,88, offerData['Agency']['Buyer Agent Commission']) #Seller's Contribution to Buyer's Broker Compensation in percentage
            
                # can.drawString(362,243, 'X') #first line buyer's agent
                # can.drawString(281,187, 'X') #second line seller's Agent
                # can.drawString(446,243, 'X') #first line dual Agent
                # can.drawString(514,243, 'X') #first line facilitator
                # can.drawString(446,187, 'X') #second line dual Agent
                # can.drawString(514,187, 'X') #second line facilitator
            
            #Realtor Commission
        elif pageNumber == 9:
            can.drawString(425, 741, today)
            can.drawString(160, 723, fullAddress)

            if offerData['Agency']['Buyer Agent Agency Type'] == 'Dual Agent': #change to check if dual agent is checked?
                can.drawString(64,630, 'X') #Dual Agency does apply (add signature block)
            else:
                can.drawString(64,648, 'X') #Dual Agency does NOT apply
        elif pageNumber == 10:
            can.drawString(425, 732, today)
            can.drawString(160, 712, fullAddress)
            # print(offerData['Offer Information']['otherContingenciesSection'])
            # can.drawString(64, 464, offerData['Offer Information']['otherContingenciesSection']) #Other Terms Line 1

            linesOfText = convertTextToMultiLine(offerData['Offer Information']['otherContingenciesSection'])
            for index, line in enumerate(linesOfText):
                # print(line)
                # print(type(index))
                if index == 0:
                    can.drawString(64, 464, line) #Other Terms Line 1
                if index == 1:
                    can.drawString(64, 446, line) #Other Terms Line 2
                if index == 2:
                    can.drawString(64, 428, line) #Other Terms Line 3
                if index == 3:
                    can.drawString(64, 410, line) #Other Terms Line 4
                if index == 4:
                    can.drawString(64, 392, line) #Other Terms Line 5
                if index == 5:
                    can.drawString(64, 374, line) #Other Terms Line 6
                if index == 6:
                    can.drawString(64, 356, line) #Other Terms Line 7
                if index == 7:
                    can.drawString(64, 338, line) #Other Terms Line 8
                if index == 8:
                    can.drawString(64, 320, line) #Other Terms Line 9

            #List of addendums.  If par of the purchase agreement, this checks the box
            # can.drawString(64, 254, 'X') # Addendum to Purchase Agreement
            # can.drawString(64, 242, 'X') # Addendum to Purchase Agreement: Additional Signatures
            # can.drawString(64, 228, 'X') # Addendum to Purchase Agreement: Assumption Financing
            # can.drawString(64, 214, 'X') # Addendum to Purchase Agreement: Buyer Move-In Agreement
            # can.drawString(64, 200, 'X') # Addendum to Purchase Agreement: Buyer Purchasing “As Is” and Limitation of Seller Liability
            # can.drawString(64, 186, 'X') # Addendum to Purchase Agreement: Condominium/Townhouse/Cooperative Common Interest Community (“CIC”)
            # can.drawString(64, 172, 'X') # Addendum to Purchase Agreement: Contract for Deed Financing
            if offerData['Offer Information']['Lead Based Paint Addendum']['Required']:
                can.drawString(64, 158, 'X') # Addendum to Purchase Agreement: Disclosure of Information on Lead-Based Paint and Lead-Based Paint Hazards
                leadBasedPaintContingencyAddendum = createLeadBasedPaintContingencyAddendum(offerData['Offer Information']['Lead Based Paint Addendum'], fullAddress)
            if offerData['Offer Information']['Sale of Buyer Property Contingency']['Option'] == '1':
                can.drawString(64, 144, 'X')
                buyerPropertyContingencyFormOptions = {
                    'address': fullAddress,
                    'contingentAddress': f'{offerData["Offer Information"]["Sale of Buyer Property Contingency"]["Property Address"]}, {offerData["Property Information"]["City"]}, {offerData["Property Information"]["State"]} {offerData["Property Information"]["Zip Code"]}',
                    'today': today, 
                    'isCurrentlyListed': offerData['Offer Information']['Sale of Buyer Property Contingency']['Is Currently Listed'],  # Whether the property is currently listed
                    'numberOfDaysToBeListed': offerData['Offer Information']['Sale of Buyer Property Contingency']['Number of Days to be Listed'],  # Number of days to be listed
                    'brokerListedWith': offerData['Offer Information']['Sale of Buyer Property Contingency']['Broker to be Listed With'],  # Broker listed with',
                    'numberOfDaysToRemoveContingencyIfSellerDemands': offerData['Offer Information']['Sale of Buyer Property Contingency']['numberOfDaysToRemoveContingencyIfSellerDemands']  # Days to remove contingency if seller demands
                }
                saleOfBuyerPropertyContingencyAddendumPdf = createSaleOfBuyerPropertyContingencyAddendum(buyerPropertyContingencyFormOptions)
                # create addendum for Sale of Buyer’s Property Contingency

            # can.drawString(64, 144, 'X') # Addendum to Purchase Agreement: Sale of Buyer’s Property Contingency
            # can.drawString(64, 130, 'X') # Addendum to Purchase Agreement: Seller’s Rent Back Agreement
            # can.drawString(64, 116, 'X') # Addendum to Purchase Agreement: Seller’s Purchase/Lease Contingency
            # can.drawString(64, 102, 'X') # Addendum to Purchase Agreement: Short Sale Contingency
            if offerData['Property Information']['Well and Septic']['Contingency']:
                can.drawString(64, 88, 'X') #Subsurface Sewage Treatment System and Well Water Inspection Contingency Addendum
                wellAndSepticContingencyAddendum = createWellAndSepticContingencyAddendum(offerData['Property Information']['Well and Septic'], fullAddress)
            # can.drawString(64, 70, 'X') #Other Addendum
            # can.drawString(115, 73, 'This is the other addendum added') #Other Addendum
        elif pageNumber == 11:
            # fillInDateAndProperty(can, today, fullAddress)#doesn't line up on this page
            can.drawString(425, 716, today)
            can.drawString(160, 694, fullAddress)

            if offerData['Property Information']['Is Seller Foreign Person']:
                can.drawString(153, 551, 'X') #Seller is a foreign person
            else:
                can.drawString(179, 551, 'X') #Seller is Not a foreign person

        can.save()
        packet.seek(0)
        try:
            newPdf = PdfReader(packet)
            page.merge_page(newPdf.pages[0]) # Merge the Sale of Buyer Property Contingency Addendum if it exists
        except IndexError:
            print(f'No content added to page number {pageNumber+1}')
        output.add_page(page)

    if saleOfBuyerPropertyContingencyAddendumPdf:
            output.add_page(saleOfBuyerPropertyContingencyAddendumPdf)  # Add the Sale of Buyer Property Contingency Addendum, single page
    if wellAndSepticContingencyAddendum:
        for i in range(2): #range(2) because the Well and Septic Contingency Addendum has 2 pages
            output.add_page(wellAndSepticContingencyAddendum[i])  # Add the Well and Septic Contingency Addendum pages
    if leadBasedPaintContingencyAddendum:
        for i in range(2): #range(2) because the Lead-Based Paint Addendum has 2 pages
            output.add_page(leadBasedPaintContingencyAddendum[i])  # Add the Well and Septic Contingency Addendum pages

    with open(savePath, 'wb') as output_stream:
        output.write(output_stream)
    return

def convertTextToMultiLine(text): #returns list of strings, each the length of one line
    lines = []
    current_line = ""
    words = re.split(r'(\s+|\r\n\r\n)', text)
    # for word in text.split():
    for word in words:
        # print(word)
        if "\r\n\r\n" in word or "\n\n" in word:
            # Add the current line and a blank line for the newline character
            if current_line.strip():
                lines.append(current_line.strip())
            lines.append("")  # Blank line for the newline
            current_line = ""
        elif len(current_line) + len(word) + 1 <= 90:
            current_line += word
        else:
            lines.append(current_line.strip())
            current_line = word.strip()
        # print(current_line)
    if current_line.strip():
        lines.append(current_line.strip())  # Add the last line

    # Limit to a maximum of 9 lines
    lines = lines[:9]
    return lines


def numberToText(number): # returns number in a string fromat from integer
    return num2words(number).capitalize()

exampleMultiLineText = 'This is an escalation clause.  Offer will be made up to $xxxxxx providedThis is an escalation clause.  Offer will be made up to $xxxxxx providedThis is an escalation clause.  Offer will be made up to $xxxxxx providedThis is an escalation clause.  THIS IS THE END OF WHERE THE SPACE SHOULD BEGIN\r\n\r\nThis is an also a clause. l be made up to $xxxxxx providedThis is an escalation clause.  Offer will be made up to $xxxxxx provided gdsfThis is an escalation clause.  Offer will be made up to $xxxxxx p'

# Split the text into lines with a max of 64 characters per line

# Join the lines back into a single string with newline characters


exampleInput = {
    'Buyer Information': {
        'Buyer 1': 'John Doe',
        'Buyer 1 Email':'',
        'Buyer 1 Phone':'',
        'Buyer 2': 'Jane Doe',
        'Buyer 2 Email':'',
        'Buyer 2 Phone':'',
        },
    'Property Information': {
        'MLS ID': '',
        'Street Address': '1331 Ashton Ct', #pull from listing data?
        'City': 'Chanhassen', #pull from listing data?
        'State': 'MN', #pull from listing data?
        'County': 'Carver', #pull from listing data?
        'Zip Code': '55317', #pull from listing data?
        'Legal Description': 'This is legally described as such', #pull from listing data? its possible to use attom api to get legal description from the property address with an api call
        'Well and Septic':{
            'Well': True,
            'Septic': True, 
            'Contingency':True,
            "Who Pays for Inspection": "Buyer", #Buyer or Seller
            "Inspection Time Period": "7", #in days
            "Inspection Scope": "Both", #Well, Septic, or Both
            }, 
        'City Water': True,
        'City Sewer': True,
        'Home Warranty': {'Added to PA':True,'To Be Obtained By':'Buyer','Paid For By':'Seller','Company Name':'Home Warranty Services, LLC','Up To Amount':'6,000'}, 
        'Is Seller Foreign Person': False,
        # 'Is There A Counteroffer': False,
        },
    'Offer Information':{
        'Purchase Price': '500,000',
        'Earnest Money': '3,000',
        'Close Date': '5/1/2025',
        # 'Terms': 'All cash offer',
        'Inspection Details':{
            'Contingent on Inspection': True,
            'Buyer Elects to Have An Inspection': True,
            'Inspection Period': '10', #if not contingent on inspection, put 0 days
            },
        'Seller Contribution': {'Seller is Contributing':True,'Seller Contribution Type': '%', 'Seller Contribution Amount': '3'}, #must only select one
        'Sale of Buyer Property Contingency' : {
            'Option': '1', 
            "Is Currently Listed": True,
            "Number of Days to be Listed": '7',
            "Broker to be Listed With": 'LPT Realty',
            "numberOfDaysToRemoveContingencyIfSellerDemands": '7',
            'Property Address': '1234 Main St',
            'Property City': 'Minneapolis',
            'Property State': 'MN',
            'Property Zip': '55418', 
            'Closing Date': '5/1/2025'},
        "Lead Based Paint Addendum": {
            "Required": True,  # This should be set to True if the year built is before 1978
            "Buyer Elects to Have Inspection": True,  # True/False, if the buyer elects to have an inspection for lead-based paint
            "Inspection Period": "10",  # This should be the number of days for the inspection period if required
            },
        #option 1 is subject to addendum, would need to add the Sale of Buyer's Property Contingency Addendum, Option 2 is PA is contingent on successful closing, Option 3 is No Contingency
        'Taxes':{'Prorated': True, 'Seller Paid Homestead Difference': True},
        'Possession': 'At Closing',
        'Seller Disclosure Received by Buyer': 'Property Disclosure Statement', #or 'Disclosure Alternatives'
        'otherContingenciesSection': exampleMultiLineText, #multiline text
        },
    'Financing': {
        'financingType': 'Conventional', # 'Conventional', 'VA', 'FHA', 'USDA', '100% Cash' #select one of these
        'ifBuyerCannotCloseEarnestMoneyWillBeGivenTo': 'Buyer', # 'Buyer' or 'Seller'
        'downPaymentPercentage': '20',
        'mortgageFinancingPercentage': '80',
        'assumingFinancingPercentage': '',
        'contractForDeedPercentage': '',
        'secondaryFinancing': 'None',
        'writtenStatement':{'required':True,'date':'6/1/2025'},
        'contingentOnFinancing': True,
        'sellerPaidLenderProcessingFees': '',
        'vaFundingFee': {'amount':'0','paidBy': 'Buyer', 'addedWhere':'At Closing'}, #va only
        'maxInterestRate': '8',
        'ifBuyerCannotSecureFinancingEarnestMoneyWillBeGivenTo': 'Buyer',
        },
    'Agency':{
        'Listing Agent Name': 'Ana Schalawamba', #pull from listing data?
        'Listing Agent Company': 'Coldwell Banker Realty', #pull from listing data?
        'Listing Agent Email': '', #pull from listing data?
        'Listing Agent Phone': '', #pull from listing data?
        'Listing Agent Agency Type': "Seller's Agent", #pull from listing data?
        'Buyer Agent Name': 'Dan Salamone',
        'Buyer Agent Company': 'LPT Group',  
        'Buyer Agent Agency Type': "Buyer's Agent",  
        'Buyer Agent Email': 'dan@email.com',  
        'Buyer Agent Phone': '162-404-1234',  
        'Buyer Agent Commission Type': '%',
        'Buyer Agent Commission': '3',
        },
}

def formatDate(dateString):
    formatted_date = datetime.strptime(dateString, '%Y-%m-%d').strftime('%m-%d-%Y')
    return formatted_date

print(formatDate('2025-05-08'))
# fillPurchaseAgreement(exampleInput)  # Example usage
# testNewPdf(exampleInput['Offer Information']['Lead Based Paint Addendum'],'C:\\Users\\salam\\Desktop\\Desktop Items\\Code\\Real Estate\\re forms\\Addendum to PA - Common Interest Community (CIC).pdf')

# createSaleOfBuyerPropertyContingencyAddendum('1331 Ashton Ct, Chanhassen, MN 55317', '1234 Main St, Minneapolis, MN 55418')  # Example usage for Sale of Buyer Property Contingency Addendum
# convertTextToMultiLine(exampleMultiLineText)