from .item import *
from .entity import *


class OrderType:
    # Do not change this enum
    ASC = 0
    DES = 1


class Statistics:
    def __init__(self, bills: list[Bill]):
        # Do not change this method
        self.bills = bills

    def find_top_sell_product(self) -> tuple [Product, int]:
        # Write here your code
        # Diccionari per comptar quantes vegades surt cada producte (per ID)
        counts = {}

        # Diccionari per guardar un Product per cada ID (per poder-lo retornar)
        products_by_id = {}

        # Recorrem totes les factures
        for bill in self.bills:
            # Recorrem tots els productes de cada factura
            for product in bill.products:
                # Agafem l'ID del producte
                pid = product.product_id

                # Comptem una aparició més d'aquest producte
                counts[pid] = counts.get(pid, 0) + 1

                # Guardem el primer Product que trobem amb aquest ID
                if pid not in products_by_id:
                    products_by_id[pid] = product

        # Si no hi ha cap producte, retornem valor buit
        if not counts:
            return (None, 0)

        # Busquem l'ID del producte que surt més vegades
        top_id = max(counts, key=counts.get)

        # Retornem el Product i el nombre d'aparicions
        return (products_by_id[top_id], counts[top_id])
        pass

    def find_top_two_sellers(self) -> list:
        # Write here your code
        # Diccionari on guardarem el total de vendes per cada venedor
        # clau   -> Seller
        # valor  -> import total de les seves vendes
        totals = {}

        # Recorrem totes les factures
        for bill in self.bills:
            # Obtenim el venedor de la factura actual
            seller = bill.seller

            # Calculem el total de la factura
            bill_total = bill.calculate_total()

            # Afegim l'import de la factura al total del venedor
            # Si el venedor no existia al diccionari, comença amb 0.0
            totals[seller] = totals.get(seller, 0.0) + bill_total

        # Convertim els venedors (claus del diccionari) en una llista
        sellers = list(totals.keys())

        # Ordenem manualment la llista de venedors segons el total venut (de major a menor)
        for i in range(len(sellers)):
            # Comparem el venedor actual amb els següents
            for j in range(i + 1, len(sellers)):
                # Si el venedor j ha venut més que el venedor i
                if totals[sellers[j]] > totals[sellers[i]]:
                    # Intercanviem les posicions
                    sellers[i], sellers[j] = sellers[j], sellers[i]

        # Retornem com a màxim els dos primers venedors de la llista ordenada
        return sellers[:2]

        
        pass

    def find_buyer_lowest_total_purchases(self) -> tuple [Buyer, float]:
        # Write here your code
        totals = {}

        for bill in self.bills:
            buyer = bill.buyer
            bill_total = bill.calculate_total()
            totals[buyer] = totals.get(buyer, 0.0) + bill_total
        
        
        if not totals:
            return (None, 0.0)   

        buyers = list(totals.keys())
        min_buyer = buyers[0]

        for i in buyers[1:]:
            if totals[i] < totals[min_buyer]:
                min_buyer = i

        return (min_buyer, totals[min_buyer])
        pass

    def order_products_by_tax(self, order_type: OrderType) -> list:
        # Write here your code
        # Agregar els impostos per product_id de totes les factures
        taxes_sum = {}
        products_by_id = {}

        for bill in self.bills:
            for product in bill.products:
                pid = product.product_id
                taxes_sum[pid] = taxes_sum.get(pid, 0.0) + product.calculate_total_taxes()
                if pid not in products_by_id:
                    products_by_id[pid] = product

        result = []
        for pid in taxes_sum:
            result.append((products_by_id[pid], taxes_sum[pid])) 

        # Ordenar manualment per taxes
        for i in range(len(result)):
            for j in range (i + 1, len(result)):
                p_i, tax_i = result[i]
                p_j, tax_j = result[j]

                if order_type == OrderType.ASC:
                    if (tax_j < tax_i) or (tax_j == tax_i and p_j.product_id < p_i.product_id):
                        result[i], result[j] = result[j], result[i]
                else:
                    if (tax_j > tax_i) or (tax_j == tax_i and _j.product_id < p_i.product_id):
                        result[i], result[j] = result[j], result[i]
        return result  
        pass

    def show(self):
        # Do not change this method
        print("Bills")
        for bill in self.bills:
            bill.print()
